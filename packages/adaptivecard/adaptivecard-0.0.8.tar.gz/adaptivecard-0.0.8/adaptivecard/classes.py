from adaptivecard.mixin import Mixin
from typing import Union, List, Optional, Any, Collection


class Element():
    pass


class TableRow(Mixin):
    def __init__(self, cells: Union["TableCell", Collection["TableCell"]]):
        if not self.is_collection(cells):
            raise TypeError("'cells' attribute must be a collection of some kind")
        if isinstance(cells, TableCell):
            cells = [cells]
        else:
            cells = list(cells)
        self.type = "TableRow"
        self.cells = cells
        self.json_fields = ("type", "cells")

    def __len__(self):
        return len(self.cells)

    def add_cell(self, cell: "TableCell"):
        if not isinstance(cell, TableCell):
            raise TypeError("'cell' attribute must be of type 'TableCell'")
        self.cells.append(cell)


class TableCell(Mixin):
    def __init__(self,
                 items: Optional[list] = None,
                 selectAction = None,   # definir mais tarde
                 style: Optional[str] = None,
                 verticalAlignment: Optional[str] = None,
                 bleed: Optional[bool] = None,
                 backgroundImage: Optional[str] = None,
                 minHeight: Optional[str] = None,
                 rtl: Optional[bool] = None):

        if items is None:
            items = []
        self.type = "TableCell"
        self.items = items
        self.selectAction = selectAction
        self.items = items
        self.style = style
        self.verticalAlignment = verticalAlignment
        self.bleed = bleed
        self.backgroundImage = backgroundImage
        self.minHeight = minHeight
        self.rtl = rtl
        self.json_fields = ('type', 'items', 'selectAction', 'style', 'verticalAlignment', 'bleed', 'backgroundImage', 'minHeight', 'rtl')

    def add_to_items(self, element: Element):
        self.items.append(element)


class Content:
    """Content é o elemento que recebe o AdaptiveCard e é adicionado à lista atachments, atributo de Message"""
    def __init__(self, content: "AdaptiveCard"):
        self.contentType = "application/vnd.microsoft.card.adaptive"
        self.content = content


class Message(Mixin):
    """"Estrutura final do card tal como se requer para envio a um canal do Teams"""
    def __init__(self, attachments: Optional[Collection["Content"]] = None):
        self.type = "message"
        if attachments is None:
            attachments = []
        if not self.is_collection(attachments):
            raise TypeError("'attachments' attribute must be a collection of some kind")
        self.attachments = list(attachments)

    def attach(self, content):
        self.attachments.append(content)

# -------------------------Cards------------------------- #


class AdaptiveCard(Mixin):
    """O template principal do card"""  # Essas descrições hão de ficar mais detalhadas à medida que eu desenvolver a lib e sua documentação
    def __init__(self, version: str = "1.2",
                 schema: str = "http://adaptivecards.io/schemas/adaptive-card.json",
                 body: Optional[Collection[Element]] = None,
                 fallbackText: Optional[str] = None,
                 backgroundImage: Optional[str] = None,
                 minHeight: Optional[str] = None,
                 rtl: Optional[bool] = None,
                 speak: Optional[str] = None,
                 lang: Optional[str] = None,
                 verticalContentAlignment: Optional[str] = None):

        if body is None:
            body = []
        if not self.is_collection(body):
            raise TypeError("'body' attribute must be a collection of some kind")
        
        self.type = "AdaptiveCard"
        self.version = version  
        self.schema = schema
        self.body = list(body)
        self.fallbackText = fallbackText
        self.backgroundImage = backgroundImage
        self.minHeight = minHeight
        self.rtl = rtl
        self.speak = speak
        self.lang = lang
        self.verticalContentAlignment = verticalContentAlignment
        self.json_fields = ('type', 'version', 'schema', 'body', 'fallbackText', 'backgroundImage',
                                      'minHeight', 'rtl', 'speak', 'lang', 'verticalContentAlignment', 'actions')

    @property
    def empty(self):
        return len(self.body) == 0

    def add_to_body(self, card_element):
        self.body.append(card_element)

    def add_action(self, action):
        if not hasattr(self, 'actions'):
            self.actions = []
        self.actions.append(action)

    def to_message(self):
        content = Content(card=self)
        msg = Message(attachments=[content])
        return msg

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'verticalContentAlignment' and isinstance(__value, str) \
                and __value not in (allowed_values := ("top", "center", "bottom")):
            raise AttributeError(f"'{__name}' atribute can only take either of the following values: {', '.join(allowed_values)}")
        return super().__setattr__(__name, __value)

# ---------------------Containers------------------------- #


class Container(Mixin):
    """Um contâiner é um agrupamento de elementos"""
    def __init__(self,
                 items: Optional[list] = None,
                 style: Optional[str] = None,
                 verticalContentAlignment: Optional[str] = None,
                 bleed: Optional[bool] = None,
                 minHeight: Optional[str] = None,
                 rtl: Optional[bool] = None,
                 height: Optional[str] = None,
                 separator: Optional[str] = None,
                 id: Optional[str] = None,
                 isVisible: Optional[bool] = None):

        if items is None:
            items = []

        self.type = "Container"
        self.items = items
        self.style = style
        self.verticalContentAlignment = verticalContentAlignment
        self.bleed = bleed
        self.minHeight = minHeight
        self.rtl = rtl
        self.height = height
        self.separator = separator
        self.id = id
        self.isVisible = isVisible
        self.json_fields = ('type', 'items', 'style', 'verticalContentAlignment', 'bleed', 'minHeight', 'rtl',
                                      'height', 'separator', 'id', 'isVisible')

    @property
    def empty(self):
        return len(self.items) == 0

    def add_to_items(self, card_element):
        self.items.append(card_element)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'style' and __value not in (allowed_values := ("default", "emphasis", "good", "attention", "warning", "accent")):
            raise AttributeError(f"'{__name}' attribute can only take either of the following values: {', '.join(allowed_values)}")
        if __name == 'verticalContentAlignment' and __value not in (allowed_values := ("top", "center", "bottom")):
            raise AttributeError(f"'{__name}' atribute can only take either of the following values: {', '.join(allowed_values)}")
        if __name == 'height' and __value not in (allowed_values := ("auto", "stretch")):
            raise AttributeError(f"'{__name}' atribute can only take either of the following values: {', '.join(allowed_values)}")
        if __name == 'spacing' and __value not in (allowed_values := ("default", "none", "small", "medium", "large", "extraLarge", "padding")):
            raise AttributeError(f"'{__name}' atribute can only take either of the following values: {', '.join(allowed_values)}")
        return super().__setattr__(__name, __value)


class ColumnSet(Mixin, Element):
    """ColumnSet define um grupo de colunas"""
    def __init__(self, columns: Optional[Collection["Column"]] = None,
                 style: Optional[str] = None,
                 bleed: Optional[bool] = None,
                 minHeight: Optional[str] = None,
                 horizontalAlignment: Optional[str] = None,
                 height: Optional[str] = None,
                 separator: Optional[bool] = None,
                 spacing: Optional[str] = None,
                 id_: Optional[str] = None,
                 isVisible: Optional[bool] = None):

        if columns is None:
            columns = []
        if not self.is_collection(columns):
            raise TypeError("'columns' attribute must be a collection of some kind")

        self.type = 'ColumnSet'
        self.columns = list(columns)
        self.style = style
        self.bleed = bleed
        self.minHeight = minHeight
        self.horizontalAlignment = horizontalAlignment
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id_
        self.isVisible = isVisible
        self.json_fields = ('type', 'columns', 'style', 'bleed', 'minHeight', 'horizontalAlignment', 'height',
                                      'separator', 'spacig', 'id', 'isVisible')

    def add_to_columns(self, column_element):
        self.columns.append(column_element)


class Column(Mixin, Element):
    """O contâiner Column define um elemento de coluna, que é parte de um ColumnSet."""
    def __init__(self,
                 items: Optional[Collection[Union["Image", "TextBlock"]]] = None,
                 backgroundImage=None,
                 bleed: Optional[bool] = None,
                 fallback: Optional["Column"] = None,
                 minHeight: Optional[str] = None,
                 rtl: Optional[bool] = None,
                 separator: Optional[bool] = None,
                 spacing: Optional[Union[str, int]] = None,
                 style: Optional[str] = None,
                 verticalContentAlignment: Optional[str] = None,
                 width: Optional[Union[str, int]] = None,
                 id_: Optional[str] = None,
                 isVisible: Optional[bool] = None):

        if items is None:
            items = []
        if self.is_collection(items):
            raise TypeError("'items' must be a collections of some kind")

        self.type = "Column"
        self.items = list(items)
        self.backgroundImage = backgroundImage
        self.bleed = bleed
        self.fallback = fallback
        self.minHeight = minHeight
        self.rtl = rtl
        self.separator = separator
        self.spacing = spacing
        self.style = style
        self.verticalContentAlignment = verticalContentAlignment
        self.width = width
        self.id = id_
        self.isVisible = isVisible
        self.json_fields = ('type', 'items', 'backgroundImage', 'bleed', 'fallback', 'minHeight', 'rtl', 'separator',
                                      'spacing', 'style', 'verticalContentAlignment', 'rtl', 'width', 'id', 'isVisible')


    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setattr__(__name, __value)

    def add_to_items(self, card_element):
        self.items.append(card_element)


class Table(Mixin, Element):
    def __init__(self,
                 columns: Collection[int],
                 rows: List[TableRow],
                 firstRowAsHeader: Optional[bool] = None,
                 showGridLines: Optional[bool] = None,
                 gridStyle: Optional[str] = None,
                 horizontalCellContentAlignment: Optional[str] = None,
                 verticalCellContentAlignment: Optional[str] = None,
                 fallback: Optional[Union["ColumnSet", "Container", "Image", "Table"]] = None,
                 height: Optional[str] = None,
                 separator: Optional[bool] = None,
                 spacing: Optional[str] = None,
                 id_: Optional[str] = None,
                 isVisible: Optional[bool] = None):

        self.type = "Table"
        if len(columns) == 0:
            raise AttributeError("Number of columns cannot be zero")
        if not self.is_collection(columns):
            raise TypeError("'columns' attribute must be a collection of some kind")
        self._columns = list(columns)
        if len(rows) == 0:
            raise Exception
        if not all(len(row) == len(columns) for row in rows):
            raise Exception("The number of cells must match the number of columns in all rows")
        self.rows = rows
        self.firstRowAsHeader = firstRowAsHeader
        self.showGridLines = showGridLines
        self.gridStyle = gridStyle
        self.horizontalCellContentAlignment = horizontalCellContentAlignment
        self.verticalCellContentAlignment = verticalCellContentAlignment
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id_
        self.isVisible = isVisible
        self.json_fields = ('type', 'columns', 'rows', 'firstRowAsHeader', 'showGridLines', 'gridStyle',
                                      'horizontalCellContentAlignment', 'verticalContentAlignment', 'fallback', 'height',
                                      'separator', 'spacing', 'id', 'isVisible')
    
    @property
    def columns(self):
        return [{"width": value} for value in self._columns]

    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setattr__(__name, __value)

# -------------------------Card Elements--------------------------- #


class TextBlock(Mixin, Element):
    """Elemento de texto"""
    def __init__(self,
                 text: str = "",
                 color: Optional[str] = None,
                 fontType: Optional[str] = None,
                 horizontalAlignment: Optional[str] = None,
                 isSubtle: Optional[bool] = None,
                 maxLines: Optional[int] = None,
                 size: Optional[str] = None,
                 weight: Optional[str] = None,
                 wrap: Optional[bool] = None,
                 style: Optional[str] = None,
                 fallback: Optional[Union[str, ColumnSet, "Container", "TextBlock"]] = None,
                 height: Optional[str] = None,
                 separator: Optional[bool] = None,
                 spacing: Optional[str] = None,
                 id_: Optional[str] = None,
                 isVisible: Optional[bool] = None):

        self.type = "TextBlock"
        self.text = text
        self.color = color
        self.fontType = fontType
        self.horizontalAlignment = horizontalAlignment
        self.isSubtle = isSubtle
        self.maxLines = maxLines
        self.size = size
        self.weight = weight
        self.wrap = wrap
        self.style = style
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id_
        self.isVisible = isVisible
        self.json_fields = ['type', 'text', 'color', 'fontType', 'horizontalAlignment', 'isSubtle', 'maxLines', 'size', 'weight', 'wrap', 'style', 'fallback',
                            'height', 'separator', 'spacing', 'id', 'isVisible']

    def __repr__(self):
        return f"{self.__class__.__name__}(text={self.text})"

    def __str__(self):
        return self.text


class Image(Mixin):
    def __init__(self,
                 url: str,
                 altText: Optional[str] = None,
                 backgroundColor: Optional[str] = None,
                 height: Optional[str] = None,
                 horizontalAlignment: Optional[str] = None,
                 selectAction: Optional[str] = None):
        self.type = "Image"
        self.json_fields = ['url', 'altText', 'backgroundColor', 'height', 'horizontalAlignment', 'selectAction']