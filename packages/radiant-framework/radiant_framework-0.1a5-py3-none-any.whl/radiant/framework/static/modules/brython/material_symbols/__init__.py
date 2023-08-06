from browser import html, document
from typing import Literal, Optional


# ----------------------------------------------------------------------
def configure(style: Literal['outined', 'rounded', 'sharp'], fill: int = 0, wght: int = 400, grad: int = 0, opsz: int = 48):
    """"""
    style = f"""
    .material-symbols-{style} {{
      font-variation-settings:
      'FILL' {fill},
      'wght' {wght},
      'GRAD' {grad},
      'opsz' {opsz}
    }}
    """
    document.select_one('head') <= html.STYLE(style)


# ----------------------------------------------------------------------
def ms(icon: str, style: Optional[Literal['outined', 'rounded', 'sharp']] = 'oulined', size: Optional[int] = None) -> html.SPAN:
    """"""
    kwargs = {}
    if size:
        kwargs = {'style': f'font-size: {size}px', }

    return html.SPAN(icon, Class=f'material-symbols-{style}', **kwargs)

