package main

import (
	"bytes"
	"flag"
	"fmt"
	"html/template"
	"io/fs"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
)

type ArchitectureConverter struct {
	inputDirs []string
	outputDir string
	htmlDir   string
	pdfDir    string
}

func NewArchitectureConverter(inputDirs []string, outputDir string) *ArchitectureConverter {
	htmlDir := filepath.Join(outputDir, "html")
	pdfDir := filepath.Join(outputDir, "pdf")
	
	os.MkdirAll(htmlDir, 0755)
	os.MkdirAll(pdfDir, 0755)
	
	return &ArchitectureConverter{
		inputDirs: inputDirs,
		outputDir: outputDir,
		htmlDir:   htmlDir,
		pdfDir:    pdfDir,
	}
}

func (ac *ArchitectureConverter) findMarkdownFiles() ([]string, error) {
	var files []string
	
	for _, inputDir := range ac.inputDirs {
		if _, err := os.Stat(inputDir); os.IsNotExist(err) {
			continue
		}
		
		err := filepath.WalkDir(inputDir, func(path string, d fs.DirEntry, err error) error {
			if err != nil {
				return err
			}
			if !d.IsDir() && strings.HasSuffix(path, ".md") {
				files = append(files, path)
			}
			return nil
		})
		
		if err != nil {
			return nil, err
		}
	}
	
	return files, nil
}

func (ac *ArchitectureConverter) findMermaidFiles() ([]string, error) {
	var files []string
	
	for _, inputDir := range ac.inputDirs {
		if _, err := os.Stat(inputDir); os.IsNotExist(err) {
			continue
		}
		
		err := filepath.WalkDir(inputDir, func(path string, d fs.DirEntry, err error) error {
			if err != nil {
				return err
			}
			if !d.IsDir() && strings.HasSuffix(path, ".mmd") {
				files = append(files, path)
			}
			return nil
		})
		
		if err != nil {
			return nil, err
		}
	}
	
	return files, nil
}

func (ac *ArchitectureConverter) renderMermaidToSVG(mermaidFile, outputSVGPath string) string {
	// Check if mermaid CLI is available
	if _, err := exec.LookPath("mmdc"); err != nil {
		return "<p>Mermaid CLI not found. Install with: npm install -g @mermaid-js/mermaid-cli</p>"
	}
	
	// Ensure output directory exists
	os.MkdirAll(filepath.Dir(outputSVGPath), 0755)
	
	// Run mermaid CLI
	cmd := exec.Command("mmdc", 
		"-i", mermaidFile,
		"-o", outputSVGPath,
		"-t", "neutral",
		"-e", "svg")
	
	if err := cmd.Run(); err != nil {
		return fmt.Sprintf("<p>Error rendering Mermaid: %v</p>", err)
	}
	
	return filepath.Base(outputSVGPath)
}

func (ac *ArchitectureConverter) processMarkdownLinks(content string, currentFile string, outputHTMLPath string) string {
	// Regex to match markdown links [text](url)
	linkRegex := regexp.MustCompile(`\[([^\]]+)\]\(([^)]+)\)`)
	
	return linkRegex.ReplaceAllStringFunc(content, func(match string) string {
		parts := linkRegex.FindStringSubmatch(match)
		if len(parts) != 3 {
			return match
		}
		
		linkText := parts[1]
		linkPath := parts[2]
		
		// Skip external links
		if strings.HasPrefix(linkPath, "http") || strings.HasPrefix(linkPath, "https") || strings.HasPrefix(linkPath, "mailto:") {
			return match
		}
		
		// Handle .mmd files - embed as SVG
		if strings.HasSuffix(linkPath, ".mmd") {
			var mmdFile string
			
			if !strings.HasPrefix(linkPath, "/") {
				// Relative path
				mmdFile = filepath.Join(filepath.Dir(currentFile), linkPath)
			} else {
				// Try to find in input directories
				for _, inputDir := range ac.inputDirs {
					candidate := filepath.Join(inputDir, strings.TrimPrefix(linkPath, "/"))
					if _, err := os.Stat(candidate); err == nil {
						mmdFile = candidate
						break
					}
				}
			}
			
			if mmdFile != "" {
				if _, err := os.Stat(mmdFile); err == nil {
					// Create SVG path next to HTML file
					svgFilename := strings.TrimSuffix(filepath.Base(mmdFile), ".mmd") + ".svg"
					svgPath := filepath.Join(filepath.Dir(outputHTMLPath), "diagrams", svgFilename)
					
					svgResult := ac.renderMermaidToSVG(mmdFile, svgPath)
					
					if strings.HasSuffix(svgResult, ".svg") {
						svgRelativePath := fmt.Sprintf("diagrams/%s", svgResult)
						return fmt.Sprintf(`
<div class="mermaid-diagram">
<img src="%s" alt="%s" />
</div>
`, svgRelativePath, linkText)
					}
					
					return svgResult
				}
			}
			
			return fmt.Sprintf(`<p>❌ Mermaid diagram not found: %s</p>`, linkPath)
		}
		
		// Convert .md to .html
		if strings.HasSuffix(linkPath, ".md") {
			linkPath = strings.TrimSuffix(linkPath, ".md") + ".html"
		}
		
		// Handle relative paths for HTML links
		if !strings.HasPrefix(linkPath, "/") {
			currentDir := filepath.Dir(currentFile)
			targetFile := filepath.Clean(filepath.Join(currentDir, linkPath))
			
			// Find which input directory contains the target file
			var targetRelPath string
			for _, inputDir := range ac.inputDirs {
				absInputDir, _ := filepath.Abs(inputDir)
				if relPath, err := filepath.Rel(absInputDir, targetFile); err == nil && !strings.HasPrefix(relPath, "..") {
					targetRelPath = relPath
					break
				}
			}
			
			if targetRelPath != "" {
				// Convert .md to .html and create path in html output directory
				if strings.HasSuffix(targetRelPath, ".md") {
					targetRelPath = strings.TrimSuffix(targetRelPath, ".md") + ".html"
				}
				
				targetHTMLPath := filepath.Join(ac.htmlDir, targetRelPath)
				
				// Calculate relative path from current HTML file to target HTML file
				if relHTMLPath, err := filepath.Rel(filepath.Dir(outputHTMLPath), targetHTMLPath); err == nil {
					linkPath = strings.ReplaceAll(relHTMLPath, "\\", "/") // normalize path separators
				}
			}
		}
		
		return fmt.Sprintf(`[%s](%s)`, linkText, linkPath)
	})
}

func (ac *ArchitectureConverter) convertMarkdownToHTML(mdFile, outputHTMLPath string) (string, error) {
	content, err := os.ReadFile(mdFile)
	if err != nil {
		return "", err
	}
	
	// Process links and embed Mermaid diagrams
	processedContent := ac.processMarkdownLinks(string(content), mdFile, outputHTMLPath)
	
	// Try pandoc first if available
	if _, err := exec.LookPath("pandoc"); err == nil {
		cmd := exec.Command("pandoc", 
			"-f", "markdown",
			"-t", "html")
		
		cmd.Stdin = strings.NewReader(processedContent)
		
		var out bytes.Buffer
		var errBuf bytes.Buffer
		cmd.Stdout = &out
		cmd.Stderr = &errBuf
		
		if err := cmd.Run(); err == nil {
			return ac.wrapInTemplate(out.String(), mdFile), nil
		}
		fmt.Printf("Pandoc failed: %s, using built-in converter\n", errBuf.String())
	}
	
	// Use built-in markdown converter
	htmlContent := ac.convertMarkdownToHTMLBuiltin(processedContent)
	return ac.wrapInTemplate(htmlContent, mdFile), nil
}

func (ac *ArchitectureConverter) convertMarkdownToHTMLBuiltin(content string) string {
	lines := strings.Split(content, "\n")
	var result []string
	var inCodeBlock bool
	var inList bool
	var listLevel int
	
	for i, line := range lines {
		originalLine := line
		line = strings.TrimSpace(line)
		
		// Code blocks
		if strings.HasPrefix(line, "```") {
			if inCodeBlock {
				result = append(result, "</code></pre>")
				inCodeBlock = false
			} else {
				lang := strings.TrimSpace(strings.TrimPrefix(line, "```"))
				if lang != "" {
					result = append(result, fmt.Sprintf(`<pre><code class="language-%s">`, lang))
				} else {
					result = append(result, "<pre><code>")
				}
				inCodeBlock = true
			}
			continue
		}
		
		// Skip processing inside code blocks
		if inCodeBlock {
			result = append(result, originalLine)
			continue
		}
		
		// Headers
		if strings.HasPrefix(line, "# ") {
			result = append(result, fmt.Sprintf("<h1>%s</h1>", strings.TrimSpace(strings.TrimPrefix(line, "#"))))
			continue
		}
		if strings.HasPrefix(line, "## ") {
			result = append(result, fmt.Sprintf("<h2>%s</h2>", strings.TrimSpace(strings.TrimPrefix(line, "##"))))
			continue
		}
		if strings.HasPrefix(line, "### ") {
			result = append(result, fmt.Sprintf("<h3>%s</h3>", strings.TrimSpace(strings.TrimPrefix(line, "###"))))
			continue
		}
		if strings.HasPrefix(line, "#### ") {
			result = append(result, fmt.Sprintf("<h4>%s</h4>", strings.TrimSpace(strings.TrimPrefix(line, "####"))))
			continue
		}
		if strings.HasPrefix(line, "##### ") {
			result = append(result, fmt.Sprintf("<h5>%s</h5>", strings.TrimSpace(strings.TrimPrefix(line, "#####"))))
			continue
		}
		if strings.HasPrefix(line, "###### ") {
			result = append(result, fmt.Sprintf("<h6>%s</h6>", strings.TrimSpace(strings.TrimPrefix(line, "######"))))
			continue
		}
		
		// Lists
		if strings.HasPrefix(line, "- ") || strings.HasPrefix(line, "* ") {
			if !inList {
				result = append(result, "<ul>")
				inList = true
				listLevel = 1
			}
			listItem := strings.TrimSpace(line[2:])
			listItem = ac.processInlineMarkdown(listItem)
			result = append(result, fmt.Sprintf("<li>%s</li>", listItem))
			continue
		}
		
		// Numbered lists
		if matched := regexp.MustCompile(`^\d+\. `).FindString(line); matched != "" {
			if !inList {
				result = append(result, "<ol>")
				inList = true
				listLevel = 1
			}
			listItem := strings.TrimSpace(strings.TrimPrefix(line, matched))
			listItem = ac.processInlineMarkdown(listItem)
			result = append(result, fmt.Sprintf("<li>%s</li>", listItem))
			continue
		}
		
		// Close lists
		if inList && line == "" {
			if listLevel == 1 {
				result = append(result, "</ul>") // or </ol>, but we'll assume ul for simplicity
			}
			inList = false
			listLevel = 0
		}
		
		// Empty lines
		if line == "" {
			continue
		}
		
		// Regular paragraphs
		line = ac.processInlineMarkdown(line)
		
		// Check if next line is a header to avoid wrapping in <p>
		nextLineIsHeader := false
		if i+1 < len(lines) {
			nextLine := strings.TrimSpace(lines[i+1])
			if strings.HasPrefix(nextLine, "#") {
				nextLineIsHeader = true
			}
		}
		
		// Don't wrap headers in paragraphs
		if !strings.HasPrefix(line, "<h") && !nextLineIsHeader {
			result = append(result, fmt.Sprintf("<p>%s</p>", line))
		} else {
			result = append(result, line)
		}
	}
	
	// Close any remaining lists
	if inList {
		result = append(result, "</ul>")
	}
	
	// Close any remaining code blocks
	if inCodeBlock {
		result = append(result, "</code></pre>")
	}
	
	return strings.Join(result, "\n")
}

func (ac *ArchitectureConverter) processInlineMarkdown(text string) string {
	// Bold **text**
	text = regexp.MustCompile(`\*\*([^*]+)\*\*`).ReplaceAllString(text, "<strong>$1</strong>")
	
	// Italic *text*
	text = regexp.MustCompile(`\*([^*]+)\*`).ReplaceAllString(text, "<em>$1</em>")
	
	// Inline code `code`
	text = regexp.MustCompile("`([^`]+)`").ReplaceAllString(text, "<code>$1</code>")
	
	// Links [text](url) - but preserve already processed ones
	text = regexp.MustCompile(`\[([^\]]+)\]\(([^)]+)\)`).ReplaceAllStringFunc(text, func(match string) string {
		parts := regexp.MustCompile(`\[([^\]]+)\]\(([^)]+)\)`).FindStringSubmatch(match)
		if len(parts) == 3 {
			linkText := parts[1]
			linkURL := parts[2]
			return fmt.Sprintf(`<a href="%s">%s</a>`, linkURL, linkText)
		}
		return match
	})
	
	return text
}

func (ac *ArchitectureConverter) wrapInTemplate(htmlContent, mdFile string) string {
	// Determine relative path
	var relativePath string
	for _, inputDir := range ac.inputDirs {
		if relPath, err := filepath.Rel(inputDir, mdFile); err == nil {
			relativePath = relPath
			break
		}
	}
	if relativePath == "" {
		relativePath = filepath.Base(mdFile)
	}
	
	title := strings.Title(strings.ReplaceAll(strings.TrimSuffix(filepath.Base(mdFile), ".md"), "-", " "))
	
	tmplStr := `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{.Title}}</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1, h2, h3, h4, h5, h6 { color: #2c3e50; }
        code { 
            background: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: "SF Mono", Monaco, "Cascadia Code", monospace;
        }
        pre { 
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        table { 
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td { 
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }
        th { background: #f8f9fa; }
        .mermaid-diagram { 
            text-align: center;
            margin: 20px 0;
        }
        .breadcrumb {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        a { color: #3498db; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="breadcrumb">
        📂 {{.RelativePath}}
    </div>
    {{.Content}}
</body>
</html>`
	
	tmpl := template.Must(template.New("page").Parse(tmplStr))
	
	var buf bytes.Buffer
	data := struct {
		Title        string
		RelativePath string
		Content      template.HTML
	}{
		Title:        title,
		RelativePath: relativePath,
		Content:      template.HTML(htmlContent),
	}
	
	tmpl.Execute(&buf, data)
	return buf.String()
}

func (ac *ArchitectureConverter) convertToHTML() error {
	fmt.Println("Converting to HTML...")
	
	mdFiles, err := ac.findMarkdownFiles()
	if err != nil {
		return err
	}
	
	for _, mdFile := range mdFiles {
		fmt.Printf("Processing %s...\n", filepath.Base(mdFile))
		
		// Determine output path - preserve directory structure
		var relPath string
		for _, inputDir := range ac.inputDirs {
			if strings.HasPrefix(mdFile, inputDir) {
				relPath, _ = filepath.Rel(inputDir, mdFile)
				break
			}
		}
		if relPath == "" {
			relPath = filepath.Base(mdFile)
		}
		
		outputPath := filepath.Join(ac.htmlDir, strings.TrimSuffix(relPath, ".md")+".html")
		os.MkdirAll(filepath.Dir(outputPath), 0755)
		
		htmlContent, err := ac.convertMarkdownToHTML(mdFile, outputPath)
		if err != nil {
			log.Printf("Error converting %s: %v", mdFile, err)
			continue
		}
		
		err = os.WriteFile(outputPath, []byte(htmlContent), 0644)
		if err != nil {
			log.Printf("Error writing %s: %v", outputPath, err)
			continue
		}
		
		fmt.Printf("  → %s\n", outputPath)
	}
	
	// Check for standalone Mermaid files
	mmdFiles, _ := ac.findMermaidFiles()
	if len(mmdFiles) > 0 {
		fmt.Printf("⚠️  Found %d standalone Mermaid files (.mmd):\n", len(mmdFiles))
		for _, mmdFile := range mmdFiles {
			fmt.Printf("    - %s\n", mmdFile)
		}
		fmt.Println("   These are ONLY converted if linked from Markdown files!")
	}
	
	return nil
}

func (ac *ArchitectureConverter) convertToPDF() error {
	fmt.Println("Converting to PDF...")
	
	err := filepath.WalkDir(ac.htmlDir, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		
		if !d.IsDir() && strings.HasSuffix(path, ".html") {
			fmt.Printf("Converting %s to PDF...\n", filepath.Base(path))
			
			relPath, _ := filepath.Rel(ac.htmlDir, path)
			pdfPath := filepath.Join(ac.pdfDir, strings.TrimSuffix(relPath, ".html")+".pdf")
			os.MkdirAll(filepath.Dir(pdfPath), 0755)
			
			// Try pandoc for PDF generation first
			cmd := exec.Command("pandoc", path, "-o", pdfPath)
			if err := cmd.Run(); err != nil {
				// Fallback: try wkhtmltopdf if available
				if _, lookErr := exec.LookPath("wkhtmltopdf"); lookErr == nil {
					cmd = exec.Command("wkhtmltopdf", path, pdfPath)
					if err := cmd.Run(); err != nil {
						log.Printf("❌ Error converting %s: %v", filepath.Base(path), err)
						return nil
					}
				} else {
					log.Printf("❌ Error converting %s: %v (no PDF engine available)", filepath.Base(path), err)
					return nil
				}
			}
			
			fmt.Printf("  → %s\n", pdfPath)
		}
		
		return nil
	})
	
	return err
}

func (ac *ArchitectureConverter) createIndexHTML() error {
	fmt.Println("Creating index.html...")
	
	// Collect all HTML files
	var htmlFiles []string
	err := filepath.WalkDir(ac.htmlDir, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		
		if !d.IsDir() && strings.HasSuffix(path, ".html") && filepath.Base(path) != "index.html" {
			relPath, _ := filepath.Rel(ac.htmlDir, path)
			htmlFiles = append(htmlFiles, relPath)
		}
		
		return nil
	})
	
	if err != nil {
		return err
	}
	
	sort.Strings(htmlFiles)
	
	// Group by directory
	byDir := make(map[string][]string)
	for _, filePath := range htmlFiles {
		dirName := filepath.Dir(filePath)
		if dirName == "." {
			dirName = "root"
		}
		byDir[dirName] = append(byDir[dirName], filePath)
	}
	
	// Create index HTML
	var dirs []string
	for dir := range byDir {
		dirs = append(dirs, dir)
	}
	sort.Strings(dirs)
	
	var content strings.Builder
	content.WriteString(fmt.Sprintf(`<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Export Documentation Index</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 8px 0; }
        a { color: #3498db; text-decoration: none; font-size: 16px; }
        a:hover { text-decoration: underline; }
        .directory { 
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .stats {
            background: #e8f5e8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>📚 Architecture Documentation</h1>
    
    <div class="stats">
        <strong>Generated:</strong> %d HTML files<br>
        <strong>Directories:</strong> %d
    </div>
`, len(htmlFiles), len(byDir)))
	
	for _, dirName := range dirs {
		files := byDir[dirName]
		sort.Strings(files)
		
		content.WriteString(fmt.Sprintf(`
    <div class="directory">
        <h2>📁 %s</h2>
        <ul>
`, dirName))
		
		for _, filePath := range files {
			name := filepath.Base(filePath)
			displayName := strings.Title(strings.ReplaceAll(strings.TrimSuffix(name, ".html"), "-", " "))
			content.WriteString(fmt.Sprintf(`            <li>📄 <a href="%s">%s</a></li>
`, filePath, displayName))
		}
		
		content.WriteString(`        </ul>
    </div>
`)
	}
	
	content.WriteString(`
    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #eee; color: #666;">
        Generated by Go Architecture Converter
    </footer>
</body>
</html>
`)
	
	indexPath := filepath.Join(ac.htmlDir, "index.html")
	err = os.WriteFile(indexPath, []byte(content.String()), 0644)
	if err != nil {
		return err
	}
	
	fmt.Printf("  → %s\n", indexPath)
	return nil
}

func (ac *ArchitectureConverter) Run(formats []string) error {
	fmt.Printf("Converting input directories: %s\n", strings.Join(ac.inputDirs, ", "))
	fmt.Printf("Output directory: %s\n", ac.outputDir)
	fmt.Printf("Formats: %s\n", strings.Join(formats, ", "))
	fmt.Println()
	
	hasHTML := false
	for _, format := range formats {
		if format == "html" {
			hasHTML = true
			break
		}
	}
	
	hasPDF := false
	for _, format := range formats {
		if format == "pdf" {
			hasPDF = true
			break
		}
	}
	
	if hasHTML || hasPDF {
		if err := ac.convertToHTML(); err != nil {
			return err
		}
		if err := ac.createIndexHTML(); err != nil {
			return err
		}
	}
	
	if hasPDF {
		if err := ac.convertToPDF(); err != nil {
			return err
		}
	}
	
	fmt.Println("\n✅ Conversion complete!")
	fmt.Printf("📁 HTML files: %s\n", ac.htmlDir)
	if hasPDF {
		fmt.Printf("📄 PDF files: %s\n", ac.pdfDir)
	}
	
	return nil
}

func main() {
	var inputDirs arrayFlags
	flag.Var(&inputDirs, "input", "Input directories (can be specified multiple times)")
	
	outputDir := flag.String("output", "converted", "Output directory")
	
	var formats arrayFlags
	flag.Var(&formats, "format", "Output formats: html, pdf (can be specified multiple times)")
	
	pdfFlag := flag.Bool("pdf", false, "Include PDF generation")
	
	flag.Parse()
	
	// Set defaults
	if len(inputDirs) == 0 {
		inputDirs = []string{"principles", "context", "design", "review", "export"}
	}
	
	if len(formats) == 0 {
		formats = []string{"html"}
		if *pdfFlag {
			formats = append(formats, "pdf")
		}
	}
	
	// Check if input directories exist
	var existingDirs []string
	for _, dir := range inputDirs {
		if _, err := os.Stat(dir); err == nil {
			existingDirs = append(existingDirs, dir)
		} else {
			fmt.Printf("⚠️  Directory not found, skipping: %s\n", dir)
		}
	}
	
	if len(existingDirs) == 0 {
		fmt.Println("❌ No input directories found")
		os.Exit(1)
	}
	
	converter := NewArchitectureConverter(existingDirs, *outputDir)
	if err := converter.Run(formats); err != nil {
		log.Fatal(err)
	}
}

// Custom flag type for string arrays
type arrayFlags []string

func (af *arrayFlags) String() string {
	return strings.Join(*af, ", ")
}

func (af *arrayFlags) Set(value string) error {
	*af = append(*af, value)
	return nil
}