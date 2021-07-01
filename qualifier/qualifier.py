from typing import Any, List, Optional
from functools import reduce
from dataclasses import dataclass, field


class Border:
    """
    U -> Upper
    B -> Bottom
    L -> Left
    R -> Right
    T -> T connector

    XC -> Cross connector
    HC -> Horizontal connector
    VC -> Vertical connector
    VCS -> Vertical connector spaced
    """

    UL = "┌"
    LL = "└"

    UR = "┐"
    LR = "┘"

    UT = "┬"
    BT = "┴"
    LT = "├"
    RT = "┤"

    HC = "─"
    VC = "│"

    XC = "┼"


@dataclass()
class Table:
    __rows: List[List[Any]]
    __labels: Optional[List[Any]] = field(default=None)
    __centered: bool = field(default=False)
    __table: List[str] = field(init=False, compare=False, default_factory=list)

    def __post_init__(self):
        self.__labels_exist: bool
        self.__str_labels: List[str]

        if self.__labels is None:
            self.__str_labels = [""] * len(self.__rows[0])
            self.__labels_exist = False
        else:
            self.__str_labels = [str(cell) for cell in self.__labels]
            self.__labels_exist = True

        self.__str_rows: List[List[str]] = [
            [str(cell) for cell in row] for row in self.__rows
        ]
        self.__max_size: List[int] = self.__get_max_lengths()

    def __get_max_lengths(self) -> List[int]:
        length_mapped_rows = map(lambda row: map(len, row), self.__str_rows)
        length_mapped_labels = map(len, self.__str_labels)

        def get_max(accu, row):
            return map(max, accu, row)

        return list(reduce(get_max, length_mapped_rows, length_mapped_labels))

    def __make_and_add_row(
        self,
        border_left: str,
        join_delim: str,
        border_right: str,
        row_data: List[Any],
        fill_char: str = " ",
    ) -> None:
        if self.__centered:
            adjusted_cells = map(
                lambda cell, size: f"{fill_char}{cell:^{size}}{fill_char}",
                row_data,
                self.__max_size,
            )
        else:
            adjusted_cells = map(
                lambda cell, size: f"{fill_char}{cell:<{size}}{fill_char}",
                row_data,
                self.__max_size,
            )

        row = f"{border_left}{join_delim.join(adjusted_cells)}{border_right}"

        self.__table.append(row)

    def make(self) -> None:
        horizontal_bars = list(
            map(lambda size: Border.HC * (size + 2), self.__max_size)
        )

        self.__make_and_add_row(
            border_left=Border.UL,
            join_delim=Border.UT,
            border_right=Border.UR,
            row_data=horizontal_bars,
            fill_char="",
        )

        if self.__labels_exist:
            self.__make_and_add_row(
                border_left=Border.VC,
                join_delim=Border.VC,
                border_right=Border.VC,
                row_data=self.__str_labels,
            )
            self.__make_and_add_row(
                border_left=Border.LT,
                join_delim=Border.XC,
                border_right=Border.RT,
                row_data=horizontal_bars,
                fill_char="",
            )

        for row in self.__str_rows:
            self.__make_and_add_row(
                border_left=Border.VC,
                join_delim=Border.VC,
                border_right=Border.VC,
                row_data=row,
            )

        self.__make_and_add_row(
            border_left=Border.LL,
            join_delim=Border.BT,
            border_right=Border.LR,
            row_data=horizontal_bars,
            fill_char="",
        )

    def __str__(self) -> str:
        return "\n".join(self.__table)


def make_table(
    rows: List[List[Any]], labels: Optional[List[Any]] = None, centered: bool = False
) -> str:
    """
    :param rows: 2D list containing objects that have a single-line representation (via `str`).
    All rows must be of the same length.
    :param labels: List containing the column labels. If present, the length must equal to that of each row.
    :param centered: If the items should be aligned to the center, else they are left aligned.
    :return: A table representing the rows passed in.
    """
    table = Table(rows, labels, centered)
    table.make()
    return str(table)
