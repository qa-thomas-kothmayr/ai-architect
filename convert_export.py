#!/usr/bin/env python3
"""
Export Converter - Convert export files to PDF and interlinked HTML with Mermaid support
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


class ExportConverter:
    def __init__(self, export_dir: str, output_dir: str):
        self.export_dir = Path(export_dir)
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
        """Find all .mmd files"""
        return list(self.export_dir.rglob("*.mmd"))
    
    def find_markdown_files(self) -> List[Path]:
        """Find all .md files"""
        return list(self.export_dir.rglob("*.md"))
    
    def render_mermaid_to_svg(self, mermaid_file: Path) -> str:
        """Convert .mmd file to SVG using mermaid CLI"""
        try:
            # Check if mermaid CLI is available
            subprocess.run(["mmdc", "--version"], 
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return f"<p>Mermaid CLI not found. Install with: npm install -g @mermaid-js/mermaid-cli</p>"
        
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tmp:
            svg_path = tmp.name
        
        try:
            subprocess.run([
                "mmdc", 
                "-i", str(mermaid_file),
                "-o", svg_path,
                "-t", "neutral"  # Use neutral theme
            ], check=True, capture_output=True)
            
            with open(svg_path, 'r') as f:
                svg_content = f.read()
            
            os.unlink(svg_path)
            return svg_content
            
        except subprocess.CalledProcessError as e:
            return f"<p>Error rendering Mermaid: {e}</p>"
    
    def process_markdown_links(self, content: str, current_file: Path) -> str:
        """Convert relative markdown links to HTML links"""
        def replace_md_link(match):
            link_text = match.group(1)
            link_path = match.group(2)
            
            # Skip external links
            if link_path.startswith(('http', 'https', 'mailto:')):
                return match.group(0)
            
            # Convert .md to .html
            if link_path.endswith('.md'):
                link_path = link_path[:-3] + '.html'
            
            # Handle relative paths
            if not link_path.startswith('/'):
                # Resolve relative to current file
                current_dir = current_file.parent
                resolved_path = (current_dir / link_path).resolve()
                
                # Make relative to export dir
                try:
                    rel_path = resolved_path.relative_to(self.export_dir.resolve())
                    link_path = str(rel_path)
                except ValueError:
                    # Path is outside export dir, leave as is
                    pass
            
            return f'[{link_text}]({link_path})'
        
        # Replace markdown links
        return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_md_link, content)
    
    def convert_markdown_to_html(self, md_file: Path) -> str:
        """Convert markdown file to HTML with enhanced features"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Process links
        content = self.process_markdown_links(content, md_file)
        
        # Setup markdown with extensions
        md = markdown.Markdown(extensions=[
            'codehilite',
            'toc',
            'tables',
            'fenced_code'
        ])
        
        html_content = md.convert(content)
        
        # Create full HTML page
        relative_path = md_file.relative_to(self.export_dir)
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
            
            html_content = self.convert_markdown_to_html(md_file)
            
            # Determine output path
            rel_path = md_file.relative_to(self.export_dir)
            output_path = self.html_dir / rel_path.with_suffix('.html')
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write HTML
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"  → {output_path}")
        
        # Process Mermaid files as standalone HTML
        for mmd_file in self.find_mermaid_files():
            print(f"Processing {mmd_file.name}...")
            
            svg_content = self.render_mermaid_to_svg(mmd_file)
            
            # Create HTML wrapper
            title = mmd_file.stem.replace('-', ' ').title()
            rel_path = mmd_file.relative_to(self.export_dir)
            
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            margin: 0;
            padding: 20px;
            text-align: center;
        }}
        .breadcrumb {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 14px;
            text-align: left;
        }}
        .diagram {{ margin: 20px auto; }}
    </style>
</head>
<body>
    <div class="breadcrumb">
        📊 {rel_path}
    </div>
    <h1>{title}</h1>
    <div class="diagram">
        {svg_content}
    </div>
</body>
</html>
            """
            
            # Determine output path
            output_path = self.html_dir / rel_path.with_suffix('.html')
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write HTML
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"  → {output_path}")
    
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
        
        # Collect all HTML files
        html_files = []
        for html_file in self.html_dir.rglob("*.html"):
            rel_path = html_file.relative_to(self.html_dir)
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
        index_content = """
<!DOCTYPE html>
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
    <h1>📚 Export Documentation</h1>
    
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
                icon = "📊" if "mmd" in str(file_path) else "📄"
                
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
        print(f"Converting export directory: {self.export_dir}")
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
    parser = argparse.ArgumentParser(description="Convert export files to PDF and HTML")
    parser.add_argument("export_dir", nargs='?', default="export", 
                       help="Export directory (default: export)")
    parser.add_argument("-o", "--output", default="converted", 
                       help="Output directory (default: converted)")
    parser.add_argument("-f", "--format", action="append", 
                       choices=["html", "pdf"], default=[],
                       help="Output formats (default: both)")
    
    args = parser.parse_args()
    
    # Default to both formats if none specified
    if not args.format:
        args.format = ["html", "pdf"]
    
    # Check if export directory exists
    if not Path(args.export_dir).exists():
        print(f"❌ Export directory not found: {args.export_dir}")
        return 1
    
    converter = ExportConverter(args.export_dir, args.output)
    converter.run(args.format)
    
    return 0


if __name__ == "__main__":
    exit(main())