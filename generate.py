from __future__ import annotations
from argparse import ArgumentParser
from dataclasses import dataclass
from functools import cached_property
from itertools import count
from pathlib import Path
from textwrap import wrap
from typing import Iterator
import svg

ROOT = Path(__file__).parent

PAGE_BG_COLOR = 'white'
CARD_FRAME_COLOR = 'red'
CARD_TEXT_COLOR = 'black'
CARD_NUMBER_COLOR = 'grey'


@dataclass
class Coord:
    page: int
    x: int
    y: int


@dataclass
class Card:
    coord: Coord
    number: int
    width: int
    height: int
    font_size: int
    text: str
    radius: int
    stroke_width: int

    def render(self) -> svg.G:
        line_height = round(self.font_size * 1.2, 2)
        lines: list[svg.Element] = []
        for line in wrap(self.text, 14):
            tspan = svg.TSpan(
                text=line,
                x=self.width // 2,
                dy=line_height,
            )
            lines.append(tspan)
        text_height = len(lines) * line_height

        r = self.radius
        return svg.G(
            transform=[
                svg.Translate(x=self.coord.x, y=self.coord.y),
            ],
            elements=[
                svg.Path(
                    fill='none',
                    stroke=CARD_FRAME_COLOR,
                    stroke_width=self.stroke_width,
                    d=[
                        svg.MoveTo(r, 0),
                        svg.LineTo(self.width - r, 0),
                        self._draw_corner(r, r),
                        svg.LineTo(self.width, self.height - r),
                        self._draw_corner(-r, r),
                        svg.LineTo(0 + r, self.height),
                        self._draw_corner(-r, -r),
                        svg.LineTo(0, r),
                        self._draw_corner(r, -r),
                    ],
                ),
                svg.Text(
                    y=self.height // 2 - text_height // 2,
                    dominant_baseline='middle',
                    text_anchor='middle',
                    fill=CARD_TEXT_COLOR,
                    font_size=self.font_size,
                    font_family='Roboto Mono, monospace',
                    elements=lines,
                ),
                svg.Text(
                    x=self.width - 5,
                    y=self.height - 5,
                    text_anchor='end',
                    fill=CARD_NUMBER_COLOR,
                    font_size=self.font_size,
                    font_family='Roboto Mono, monospace',
                    text=str(self.number),
                ),
            ],
        )

    def _draw_corner(self, dx: int, dy: int) -> svg.ArcRel:
        """Produce an arc for rounded corner
        """
        return svg.ArcRel(
            rx=self.radius,
            ry=self.radius,
            angle=0,
            large_arc=False,
            sweep=True,
            dx=dx, dy=dy,
        )


@dataclass
class Generator:
    page_width: int
    page_height: int
    card_width: int
    card_height: int
    border: int
    padding: int
    corner_radius: int
    stroke_width: int
    font_size: int
    output: Path

    def save_all(self) -> None:
        self.output.mkdir(exist_ok=True)
        for page_number in self.pages:
            out_path = self.output / f'{page_number}.svg'
            page_svg = self.generate_page(page_number)
            out_path.write_text(str(page_svg))

    def generate_page(self, page_number: int) -> svg.SVG:
        return svg.SVG(
            viewBox=svg.ViewBoxSpec(0, 0, self.page_width, self.page_height),
            width=svg.mm(self.page_width),
            height=svg.mm(self.page_height),
            elements=list(self.iter_cards(page_number)),
        )

    def iter_cards(self, page_number: int) -> Iterator[svg.Element]:
        yield svg.Defs(elements=[
            svg.Style(
                text='@import url("https://fonts.googleapis.com/css?family=Roboto+Mono:400");',
            ),
        ])
        yield svg.Rect(
            x=0, y=0,
            width=self.page_width,
            height=self.page_height,
            fill=PAGE_BG_COLOR,
        )
        for card in self.cards:
            if card.coord.page == page_number:
                yield card.render()

    @property
    def pages(self) -> Iterator[int]:
        prev_page = -1
        for card in self.cards:
            if card.coord.page != prev_page:
                yield card.coord.page
                prev_page = card.coord.page

    @cached_property
    def cards(self) -> list[Card]:
        """List of all cards to render.
        """
        cards = []
        phrases = (ROOT / 'phrases.txt').read_text().strip().splitlines()
        card_number = count(1)
        for coord, phrase in zip(self.iter_coords(), phrases):
            cards.append(Card(
                coord=coord,
                number=next(card_number),
                text=phrase,
                width=self.card_width,
                height=self.card_height,
                font_size=self.font_size,
                radius=self.corner_radius,
                stroke_width=self.stroke_width,
            ))
        return cards

    def iter_coords(self) -> Iterator[Coord]:
        """Infinite iterator producing coordinates for cards.

        Alright, it's capped to 100 pages, but that's just a precaution.
        """
        step_x = self.card_width + self.padding
        step_y = self.card_height + self.padding
        right_stop = self.page_width - step_x - self.border
        bottom_stop = self.page_height - step_y - self.border
        for page in range(1, 100):
            for y in range(self.border, bottom_stop, step_y):
                for x in range(self.border, right_stop, step_x):
                    yield Coord(page=page, x=x, y=y)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        '--page-width', type=int, default=210,
        help='horizontal size of each page',
    )
    parser.add_argument(
        '--page-height', type=int, default=297,
        help='vertical size of each page',
    )
    parser.add_argument(
        '--card-width', type=int, default=60,
        help='horizontal size of each card',
    )
    parser.add_argument(
        '--card-height', type=int, default=90,
        help='vertical size of each card',
    )
    parser.add_argument(
        '--border', type=int, default=5,
        help='distance to keep from each page edge',
    )
    parser.add_argument(
        '--padding', type=int, default=2,
        help='distance between cards',
    )
    parser.add_argument(
        '--font-size', type=int, default=6,
        help='size of the font for text on cards',
    )
    parser.add_argument(
        '--corner-radius', type=int, default=5,
        help='radius of the corner for each card frame',
    )
    parser.add_argument(
        '--stroke-width', type=int, default=1,
        help='line width for card frames',
    )
    parser.add_argument(
        '--output', type=Path, default=ROOT / 'build',
        help='path where to write generated pages',
    )
    args = parser.parse_args()
    generator = Generator(**vars(args))
    generator.save_all()


if __name__ == '__main__':
    main()
