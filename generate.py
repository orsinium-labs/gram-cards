from __future__ import annotations
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap
from typing import Iterator
import svg

ROOT = Path(__file__).parent


@dataclass
class Generator:
    page_width: int
    page_height: int
    card_width: int
    card_height: int
    border: int
    padding: int
    font_size: int
    output: Path

    def save_all(self) -> None:
        self.output.mkdir(exist_ok=True)
        (self.output / '1.svg').write_text(str(self.generate_page()))

    def generate_page(self) -> svg.SVG:
        return svg.SVG(
            width=self.page_width,
            height=self.page_height,
            elements=list(self.iter_cards()),
        )

    def iter_cards(self) -> Iterator[svg.Element]:
        yield svg.Defs(elements=[
            svg.Style(
                text='@import url("https://fonts.googleapis.com/css?family=Roboto+Mono:400");',
            ),
        ])
        yield svg.Rect(x=0, y=0, width=self.page_width, height=self.page_height, fill='grey')
        phrases = (ROOT / 'phrases.txt').read_text().splitlines()
        step = self.card_width + self.padding
        right_stop = self.page_width - step - self.border
        for x in range(self.border, right_stop, step):
            yield self.draw_card(x=x, y=0, text=phrases[0])

    def draw_card(self, x: int, y: int, text: str) -> svg.Element:
        line_height = round(self.font_size * 1.2, 2)
        lines: list[svg.Element] = []
        for line in wrap(text, 14):
            tspan = svg.TSpan(
                text=line,
                x=self.card_width // 2,
                dy=line_height,
            )
            lines.append(tspan)
        text_height = len(lines) * line_height

        return svg.G(
            transform=[svg.Translate(x=x, y=y)],
            elements=[
                svg.Rect(
                    x=0, y=0,
                    width=self.card_width,
                    height=self.card_height,
                    stroke='red',
                    fill='none',
                ),
                svg.Text(
                    y=self.card_height // 2 - text_height // 2,
                    dominant_baseline='middle',
                    text_anchor='middle',
                    fill='black',
                    font_size=self.font_size,
                    font_family='Roboto Mono, monospace',
                    elements=lines,
                ),
            ],
        )


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('--page-width', type=int, default=210)
    parser.add_argument('--page-height', type=int, default=297)
    parser.add_argument('--card-width', type=int, default=60)
    parser.add_argument('--card-height', type=int, default=90)
    parser.add_argument('--border', type=int, default=5)
    parser.add_argument('--padding', type=int, default=2)
    parser.add_argument('--font-size', type=int, default=6)
    parser.add_argument('--output', type=Path, default=ROOT / 'build')
    args = parser.parse_args()
    generator = Generator(**vars(args))
    generator.save_all()


if __name__ == '__main__':
    main()
