from mistletoe import Document
from md2site.renderer import Renderer


r = Renderer("https://2501.sh")
html = r.render(Document("[[page 1]], [[page 2 | display text for link 2]]"))
print(html)
