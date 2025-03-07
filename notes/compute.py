import markdown
import re
import os

def convert_md_to_html(md_file, output_html):
    with open(md_file, "r", encoding="utf-8") as file:
        md_content = file.read()
    
    # Convert Markdown to HTML (with code blocks and tables enabled)
    html_content = markdown.markdown(md_content, extensions=["fenced_code", "tables"])

    # Manually replace LaTeX equations with MathJax-compatible syntax
    # Block Equations: $$...$$ → <div class="math">\[...\]</div>
    html_content = re.sub(r'\$\$(.*?)\$\$', r'<div class="math">\\[\1\\]</div>', html_content, flags=re.DOTALL)

    # Inline Equations: $...$ → <span class="math">\( ... \)</span>
    html_content = re.sub(r'\$(.*?)\$', r'<span class="math">\\(\1\\)</span>', html_content)

    # Find and wrap images in a responsive Bootstrap class
    html_content = re.sub(
        r'<img(.*?)src="(.*?)"(.*?)>',
        r'<div class="text-center"><img class="img-fluid rounded shadow mt-3 mb-3" src="\2" \1 \3></div>',
        html_content
    )

    match = re.search(r'\\(.*?)\\', md_file)
    title = match.group(1) if match else "Unknown"

    # A modern Bootstrap-based template
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Aliaksandr Melnichenka Personal Website</title>
        <link rel="icon" href="../../img/favicon.ico" />

        <!-- Google Font -->
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link
            href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
            rel="stylesheet"
        />

        <!-- Bootstrap CSS -->
        <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
        />

        <!-- MathJax -->
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script
            id="MathJax-script"
            async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
        ></script>

        <style>
            body {{
                font-family: 'Inter', sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 0;
            }}
            .navbar {{
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            }}
            .hero-section {{
                background: linear-gradient(135deg, #007bff 0%, #6610f2 100%);
                color: #fff;
                padding: 4rem 0;
                text-align: center;
                margin-bottom: 2rem;
            }}
            .hero-section h1 {{
                font-size: 2.5rem;
                font-weight: 600;
                margin-bottom: 1rem;
            }}
            .hero-section p {{
                font-size: 1.2rem;
                margin-bottom: 0;
            }}
            .content-container {{
                max-width: 900px;
                margin: 0 auto;
                padding: 1rem;
            }}
            .math {{
                color: #000;
                font-size: 1.05em;
            }}
            h1, h2, h3, h4, h5, h6 {{
                margin-top: 1.5rem;
                margin-bottom: 0.75rem;
            }}
            p {{
                margin-bottom: 1rem;
                line-height: 1.6;
            }}
            pre {{
                background: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                margin-bottom: 1rem;
            }}
            code {{
                color: #000;
                font-weight: 600;
                font-size: 0.95rem;
            }}
            footer {{
                background-color: #f1f1f1;
                text-align: center;
                padding: 10px 0;
                margin-top: 2rem;
            }}
            .footer-text {{
                margin: 0;
                color: #6c757d;
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <!-- Navigation Bar (Fixed-top for a modern sticky header) -->
        <nav class="navbar navbar-expand-lg navbar-light bg-light sticky-top">
          <div class="container">
            <a class="navbar-brand fw-bold" href="#">My Public Notes</a>
            <button
              class="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarContent"
              aria-controls="navbarContent"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarContent">
              <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                <li class="nav-item">
                  <a class="nav-link active" aria-current="page" href="https://melnichenka.com/">Home</a>
                </li>
                <!-- Add more nav links as needed -->
              </ul>
            </div>
          </div>
        </nav>

        <!-- Main Content -->
        <div class="content-container p-4">
            <h3 class="text-3xl font-bold text-gray-800 bg-gradient-to-r from-blue-500 to-purple-500 text-black rounded-lg shadow-md">
                Notes @ {title}
            </h3>
            {html_content}
        </div>

        <!-- Footer -->
        <footer>
            <p class="footer-text">© 2025 Aliaksandr Melnichenka Personal Website</p>
        </footer>

        <!-- Bootstrap JS -->
        <script
            src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
        ></script>
    </body>
    </html>
    """

    with open(output_html, "w", encoding="utf-8") as file:
        file.write(html_template)

    print(f"HTML file saved as {output_html}")


def convert_all_md_in_folder(root_folder):
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(subdir, file)
                html_file_path = os.path.splitext(md_file_path)[0] + ".html"
                convert_md_to_html(md_file_path, html_file_path)

# Example usage: Convert all Markdown files in the current directory and subdirectories
convert_all_md_in_folder(".")
