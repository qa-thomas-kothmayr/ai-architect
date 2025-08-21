#!/usr/bin/env python3
"""
Architecture Documentation Converter - Convert architecture documentation to PDF and interlinked HTML with Mermaid support
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import subprocess
import tempfile

# Dependencies check
try:
    import markdown
    from markdown.extensions import codehilite, toc
except ImportError:
    print("Please install: pip install markdown")
    exit(1)

try:
    import weasyprint
except ImportError:
    print("Please install: pip install weasyprint")
    exit(1)


class ArchitectureConverter:
    def __init__(self, input_dirs: List[str], output_dir: str):
        self.input_dirs = [Path(d) for d in input_dirs]
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirs
        self.html_dir = self.output_dir / "html"
        self.pdf_dir = self.output_dir / "pdf"
        self.html_dir.mkdir(exist_ok=True)
        self.pdf_dir.mkdir(exist_ok=True)
        
        # Track all files for interlinking
        self.all_files: Dict[str, str] = {}
        
    def find_mermaid_files(self) -> List[Path]:
        """Find all .mmd files in input directories"""
        files = []
        for input_dir in self.input_dirs:
            if input_dir.exists():
                files.extend(list(input_dir.rglob("*.mmd")))
        return files
    
    def find_markdown_files(self) -> List[Path]:
        """Find all .md files in input directories"""
        files = []
        for input_dir in self.input_dirs:
            if input_dir.exists():
                files.extend(list(input_dir.rglob("*.md")))
        return files
    
    def render_mermaid_to_svg(self, mermaid_file: Path, output_svg_path: Path) -> str:
        """Convert .mmd file to SVG using mermaid CLI and save to output location"""
        try:
            # Check if mermaid CLI is available
            subprocess.run(["mmdc", "--version"], 
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return f"<p>Mermaid CLI not found. Install with: npm install -g @mermaid-js/mermaid-cli</p>"
        
        # Ensure output directory exists
        output_svg_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            subprocess.run([
                "mmdc", 
                "-i", str(mermaid_file),
                "-o", str(output_svg_path),
                "-t", "neutral",  # Use neutral theme
                "-e", "svg",      # Embed fonts and images for standalone SVG
                "--puppeteerConfigFile", ".puppeteerConfigFile" # workaround sandbox
            ], check=True, capture_output=True)
            
            # Return relative path from HTML to SVG for embedding
            return str(output_svg_path.name)
            
        except subprocess.CalledProcessError as e:
            return f"<p>Error rendering Mermaid: {e}</p>"
    
    def process_markdown_links(self, content: str, current_file: Path, output_html_path: Path) -> str:
        """Convert relative markdown links to HTML links and embed Mermaid diagrams"""
        def replace_md_link(match):
            link_text = match.group(1)
            link_path = match.group(2)
            
            # Skip external links
            if link_path.startswith(('http', 'https', 'mailto:')):
                return match.group(0)
            
            # Handle .mmd files - embed as SVG instead of linking
            if link_path.endswith('.mmd'):
                # Resolve the mermaid file path
                mmd_file = None
                if not link_path.startswith('/'):
                    mmd_file = current_file.parent / link_path
                else:
                    # Try to find in any input directory
                    for input_dir in self.input_dirs:
                        candidate = input_dir / link_path.lstrip('/')
                        if candidate.exists():
                            mmd_file = candidate
                            break
                
                if mmd_file and mmd_file.exists():
                    # Create SVG path next to HTML file
                    svg_filename = mmd_file.stem + '.svg'
                    svg_path = output_html_path.parent / 'diagrams' / svg_filename
                    
                    svg_result = self.render_mermaid_to_svg(mmd_file, svg_path)
                    
                    if svg_result.endswith('.svg'):
                        # Success - reference the SVG file
                        svg_relative_path = f"diagrams/{svg_result}"
                        return f'\n<div class="mermaid-diagram">\n<img src="{svg_relative_path}" alt="{link_text}" />\n</div>\n'
                    else:
                        # Error message from render function
                        return svg_result
                else:
                    # Debug information
                    debug_info = f"Searched paths:\n"
                    if not link_path.startswith('/'):
                        debug_path = current_file.parent / link_path
                        debug_info += f"  - Relative: {debug_path} (exists: {debug_path.exists()})\n"
                    else:
                        for input_dir in self.input_dirs:
                            debug_path = input_dir / link_path.lstrip('/')
                            debug_info += f"  - {input_dir.name}: {debug_path} (exists: {debug_path.exists()})\n"
                    return f'<p>❌ Mermaid diagram not found: {link_path}</p><pre>{debug_info}</pre>'
            
            # Convert .md to .html
            if link_path.endswith('.md'):
                link_path = link_path[:-3] + '.html'
            
            # Handle relative paths
            if not link_path.startswith('/'):
                # Resolve the target file relative to current file
                current_dir = current_file.parent
                target_file = (current_dir / link_path).resolve()
                
                # Convert target file to its HTML output path
                target_html_path = None
                for input_dir in self.input_dirs:
                    try:
                        target_rel_path = target_file.relative_to(input_dir)
                        target_html_path = self.html_dir / target_rel_path.with_suffix('.html')
                        break
                    except ValueError:
                        continue
                
                if target_html_path:
                    # Calculate relative path from current HTML file to target HTML file
                    try:
                        link_path = os.path.relpath(target_html_path, output_html_path.parent)
                    except ValueError:
                        # Fallback to absolute path within HTML dir
                        link_path = str(target_html_path.relative_to(self.html_dir))
            
            return f'[{link_text}]({link_path})'
        
        # Replace markdown links
        return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_md_link, content)
    
    def convert_markdown_to_html(self, md_file: Path, output_html_path: Path) -> str:
        """Convert markdown file to HTML with enhanced features"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Process links and embed Mermaid diagrams
        content = self.process_markdown_links(content, md_file, output_html_path)
        
        # Setup markdown with extensions
        md = markdown.Markdown(extensions=[
            'codehilite',
            'toc',
            'tables',
            'fenced_code'
        ])
        
        html_content = md.convert(content)
        
        # Create full HTML page
        # Find which input dir contains this file
        relative_path = None
        for input_dir in self.input_dirs:
            try:
                relative_path = md_file.relative_to(input_dir)
                break
            except ValueError:
                continue
        
        if relative_path is None:
            relative_path = md_file.name  # fallback
        
        title = md_file.stem.replace('-', ' ').title()
        
        full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3, h4, h5, h6 {{ color: #2c3e50; }}
        code {{ 
            background: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: "SF Mono", Monaco, "Cascadia Code", monospace;
        }}
        pre {{ 
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        table {{ 
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{ 
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{ background: #f8f9fa; }}
        .mermaid-diagram {{ 
            text-align: center;
            margin: 20px 0;
        }}
        .breadcrumb {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="breadcrumb">
        📂 {relative_path}
    </div>
    {html_content}
</body>
</html>
        """
        
        return full_html
    
    def convert_to_html(self):
        """Convert all files to HTML"""
        print("Converting to HTML...")
        
        # Process markdown files
        for md_file in self.find_markdown_files():
            print(f"Processing {md_file.name}...")
            
            # Determine output path - preserve directory structure from input dirs
            rel_path = None
            for input_dir in self.input_dirs:
                try:
                    file_rel_path = md_file.relative_to(input_dir)
                    # Preserve the original directory structure relative to input dir
                    rel_path = file_rel_path
                    break
                except ValueError:
                    continue
            
            if rel_path is None:
                rel_path = Path(md_file.name)  # fallback
            
            output_path = self.html_dir / rel_path.with_suffix('.html')
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            html_content = self.convert_markdown_to_html(md_file, output_path)
            
            # Write HTML
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"  → {output_path}")
        
        # Find standalone Mermaid files
        mermaid_files = self.find_mermaid_files()
        if mermaid_files:
            print(f"⚠️  Found {len(mermaid_files)} standalone Mermaid files (.mmd):")
            for mmd_file in mermaid_files:
                print(f"    - {mmd_file}")
            print("   These are ONLY converted if linked from Markdown files!")
            print("   Standalone .mmd files are currently not processed separately.")
        else:
            print("Note: Mermaid files (.mmd) are only converted when referenced in Markdown files")
    
    def convert_to_pdf(self):
        """Convert HTML files to PDF"""
        print("Converting to PDF...")
        
        for html_file in self.html_dir.rglob("*.html"):
            print(f"Converting {html_file.name} to PDF...")
            
            # Determine output path
            rel_path = html_file.relative_to(self.html_dir)
            pdf_path = self.pdf_dir / rel_path.with_suffix('.pdf')
            pdf_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                # Use weasyprint for PDF generation
                weasyprint.HTML(filename=str(html_file)).write_pdf(str(pdf_path))
                print(f"  → {pdf_path}")
            except Exception as e:
                print(f"  ❌ Error converting {html_file.name}: {e}")
    
    def create_index_html(self):
        """Create an index file linking to all converted files"""
        print("Creating index.html...")
        
        # Collect all HTML files (excluding standalone Mermaid HTML files)
        html_files = []
        for html_file in self.html_dir.rglob("*.html"):
            rel_path = html_file.relative_to(self.html_dir)
            # Only include files that come from .md sources
            md_found = False
            for input_dir in self.input_dirs:
                corresponding_md = input_dir / rel_path.with_suffix('.md')
                if corresponding_md.exists():
                    md_found = True
                    break
            
            if md_found or html_file.name == 'index.html':
                html_files.append(rel_path)
        
        html_files.sort()
        
        # Group by directory
        by_dir = {}
        for file_path in html_files:
            dir_name = str(file_path.parent) if file_path.parent != Path('.') else 'root'
            if dir_name not in by_dir:
                by_dir[dir_name] = []
            by_dir[dir_name].append(file_path)
        
        # Create index HTML
        index_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Export Documentation Index</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 8px 0; }}
        a {{ color: #3498db; text-decoration: none; font-size: 16px; }}
        a:hover {{ text-decoration: underline; }}
        .directory {{ 
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .stats {{
            background: #e8f5e8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <h1>📚 Architecture Documentation</h1>
    
    <div class="stats">
        <strong>Generated:</strong> {len(html_files)} HTML files<br>
        <strong>Directories:</strong> {len(by_dir)}
    </div>
"""
        
        for dir_name in sorted(by_dir.keys()):
            files = by_dir[dir_name]
            
            index_content += f"""
    <div class="directory">
        <h2>📁 {dir_name}</h2>
        <ul>
"""
            
            for file_path in sorted(files):
                name = file_path.name
                display_name = name.replace('-', ' ').replace('.html', '').title()
                
                # Add icon based on file type  
                icon = "📄"  # All files are now Markdown-based
                
                index_content += f'            <li>{icon} <a href="{file_path}">{display_name}</a></li>\n'
            
            index_content += """        </ul>
    </div>
"""
        
        index_content += """
    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #eee; color: #666;">
        Generated by Export Converter
    </footer>
</body>
</html>
        """
        
        # Write index
        index_path = self.html_dir / "index.html"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"  → {index_path}")
    
    def run(self, format_types: List[str]):
        """Run the conversion process"""
        print(f"Converting input directories: {', '.join(str(d) for d in self.input_dirs)}")
        print(f"Output directory: {self.output_dir}")
        print(f"Formats: {', '.join(format_types)}")
        print()
        
        if 'html' in format_types:
            self.convert_to_html()
            self.create_index_html()
        
        if 'pdf' in format_types:
            if 'html' not in format_types:
                # Need HTML first
                self.convert_to_html()
            self.convert_to_pdf()
        
        print("\n✅ Conversion complete!")
        print(f"📁 HTML files: {self.html_dir}")
        if 'pdf' in format_types:
            print(f"📄 PDF files: {self.pdf_dir}")


def main():
    parser = argparse.ArgumentParser(description="Convert architecture documentation to PDF and HTML")
    parser.add_argument("input_dirs", nargs='*', 
                       default=["principles", "context", "design", "review", "export"],
                       help="Input directories (default: principles context design review export)")
    parser.add_argument("-o", "--output", default="converted", 
                       help="Output directory (default: converted)")
    parser.add_argument("-f", "--format", action="append", 
                       choices=["html", "pdf"], default=[],
                       help="Output formats (default: html only, use --pdf to include PDF)")
    parser.add_argument("--pdf", action="store_true",
                       help="Include PDF generation (requires weasyprint)")
    
    args = parser.parse_args()
    
    # Determine formats
    if not args.format:
        args.format = ["html"]
        if args.pdf:
            args.format.append("pdf")
    
    # Check if any input directories exist
    existing_dirs = []
    for dir_path in args.input_dirs:
        if Path(dir_path).exists():
            existing_dirs.append(dir_path)
        else:
            print(f"⚠️  Directory not found, skipping: {dir_path}")
    
    if not existing_dirs:
        print("❌ No input directories found")
        return 1
    
    converter = ArchitectureConverter(existing_dirs, args.output)
    converter.run(args.format)
    
    return 0


if __name__ == "__main__":
    exit(main())
