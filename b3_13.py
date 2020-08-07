import textwrap

class TopLevelTag:
    # ...
    def __init__(self, tag, toplevel=False, klass=None):
        self.tag = tag
        self.toplevel = toplevel
        # Словарь с атрибутами
        self.attributs = {}
        # Список внутренних тегов
        self.childrens = []
        self.attrs = []

        if klass is not None:
            self.attributs['class'] = ' '.join(klass)

        for attr, val in self.attributs.items():
            val = val.replace('_', '-')
            self.attrs.append('%s ="%s"' % (attr, val))

        self.attrs = " ".join(self.attrs)

    # Метод для +=
    def __iadd__(self, other):
        self.childrens.append(other)
        return self

    def __str__(self, *args):
        html = "<%s>" % self.tag
        for child in self.childrens:
            html += "\n" + textwrap.indent(str(child), "    ")
        html += "\n" + "</%s>" % self.tag
        return html

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self

class HTML:

    # ...
    def __init__(self, output=None):
        self.output = output
        # Словарь с атрибутами
        self.attributs = {}
        # Список внутренних тегов
        self.children = []

    # Метод для +=
    def __iadd__(self, other):
        self.children.append(other)
        return self

    # Методы для контекстного менеджера
    # Просто возвращаем сам объект в начале
    def __enter__(self):
        return self

    def __exit__(self, *args):
        # Если указан output то запишем в файл
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        # Если нет, то просто выведем
        else:
            print(self)

        # Метод, который вызывается при использовании str
    def __str__(self, *args):
        # Открывающий тег
        html = "<html>"
        # Содержимое
        for child in self.children:
            html += "\n" + textwrap.indent(str(child), "    ")
        # Закрывающий
        html += "\n</html>"
        return html


class Tag:

    # Объявим метод конструктора
    # klass - кортеж с классами
    def __init__(self, tag, is_single=False, toplevel=False, klass=None, **kwargs):
        self.tag = tag
        self.is_single = is_single
        self.toplevel = toplevel
        self.text = ""

        # Словарь с атрибутами
        self.attributs = {}

        # Список внутренниъ тегов
        self.childrens = []
        self.attrs = []
        # Если есть классы у тега, добавим атрибут class и значение атрибута - элементы кортежа через пробел
        if klass is not None:
            self.attributs['class'] = ' '.join(klass)

        for attr, val in kwargs.items():
            attr = attr.replace('_', '-')
            self.attributs[attr] = val

        # Метод для +=

    def __iadd__(self, other):
        self.childrens.append(other)
        return self

    def __str__(self, *args):
        self.attrs = []
        for attr, val in self.attributs.items():
            self.attrs.append('%s="%s"' % (attr, val))
        self.attrs = " ".join(self.attrs)

        # Если тег single
        if self.is_single:
            return "<{tag} {attrs}/>".format(tag=self.tag, attrs=self.attrs)
        # Если у тега нет внутренних элементов
        elif not self.attrs:
            return "<{tag}>{text}<{tag}\>".format(tag=self.tag, text=self.text)
        # Если у тега есть внутренние элементы
        else:
            # Открываем тег
            html = "<{tag} {attrs}>".format(tag=self.tag, attrs=self.attrs)
            # Если есть текст внутри, с новой строки добавляем текст
            if self.text:
                # Тут просто перед текстом добавим табуляцию
                html += "\n    " + self.text
                # Добавляем код внутренних элементов с новой строки каждый
            for child in self.childrens:
                # Тут добавим табуляцию к str(child)
                html += "\n" + textwrap.indent(str(child), "    ")
                # С новой строки закрывающий тег
            html += "\n</{tag}>".format(tag=self.tag)
            return html

    # Методы для контекстного менеджера
    # Просто возвращаем сам объект в начале
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self

if __name__ == "__main__":
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p", id="text") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", href="", is_single=True, src="image/icon.png", data_image="responsive", alt="img test") as img:
                    div += img

                body += div

            doc += body
