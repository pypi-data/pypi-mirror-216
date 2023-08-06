import oimdp
from oimdp.structures import *
from lxml import etree
from lxml.etree import Element
from typing import TypedDict

from oitei.tei_template import TEI_TEMPLATE, DECLS
from oitei.namespaces import TEINS, NS


class Metadata(TypedDict):
    prefix: str
    idno: str
    auth_uri: str
    author: str
    book_uri: str
    book: str


class Converter:
    """OpenITI mARkdown to OpenITI TEI converter"""
    # TODO: allow users to provide template or at least URL to schema
    def __init__(self, text: str, metadata: Metadata):
        self.magic_value = "######OpenITI#"
        self.doc = etree.fromstring(TEI_TEMPLATE)
        self.context_linepart = None
        self.metadata = metadata
        
        try:
            self.context_node = self.doc.find(".//tei:body", NS)
            self.body = self.context_node
        except Exception:
            raise Exception("Could not initiate TEI document.") 

        try:
            self.md = oimdp.parse(text)
        except Exception:
            raise Exception("Could not parse mARkdown document.") 

        if not str(self.md.magic_value).startswith(self.magic_value):
            raise Exception("Text provided does not appear to be a valid mARkdown document.") 


    def __str__(self):

        space = "  "

        def text_indent(el, level=0, islast=False):
            """ Indent text nodes despite etree's nonesensical insistence that doing so alters data.
                (any sequence of spaces is one space in XML unless xml:space="preserve" is specified) """
            xml_space = el.get("{http://www.w3.org/XML/1998/namespace}space")
            if xml_space != "preserve":
                if str(el.tail).endswith("\n"):
                    indent = level * space
                    if islast:
                        indent = (level-1) * space
                    el.tail = el.tail + indent
                tot_children = len(el)
                if tot_children:
                    for count, child in enumerate(el):
                        text_indent(child, level+1, count+1 == tot_children)

        if self.doc is not None:
            etree.indent(self.doc, space=space)
            text_indent(self.doc)
                    
            tree_str = etree.tostring(self.doc, xml_declaration=False, pretty_print=True, encoding="UTF-8").decode("utf-8")
            return DECLS + tree_str
        else:
            return ""

    
    def tostring(self):
        return self.__str__()


    def _appendText(self, el: Element, text: str):
        children = el.getchildren()
        if len(children) > 0:
            tail = children[-1].tail
            if tail:
                children[-1].tail = tail + text
            else:
                children[-1].tail = text
        else:
            if el.text:
                el.text = el.text + text
            else:
                el.text = text


    def _pagenum_lookdown(self, pos):
        for c in self.md.content[pos:]:
            if isinstance(c, PageNumber) or isinstance(c, Line):
                if isinstance(c, Line):
                    for lp in c.parts:
                        if isinstance(lp, PageNumber):
                            return lp
                elif isinstance(c, PageNumber):
                    return c


    def _create_pb(self, c):
        if c:
            pb = etree.SubElement(self.context_node, f"{TEINS}pb")
            value = ""
            if c.volume.isdigit():
                if int(c.volume) > 0:
                    value += f"Vol. {int(c.volume)}, "
            else:
                value += f"Vol. {c.volume}, "
            page = c.page
            if page.isdigit():
                page = int(page)
            value += f"p. {page}"
            pb.set("n", value)


    def convert(self):
        # Set up TEI document from a minimal string template
        teiHeader = self.doc.find(".//tei:teiHeader", NS)

        # Inject author and book level metadata if provided
        if self.metadata:
            pub = teiHeader.find(".//tei:publicationStmt", NS)
            idno = etree.SubElement(pub, "idno")
            idno.text = self.metadata["idno"]

            title = teiHeader.find(".//tei:titleStmt/tei:title", NS)
            title.set("ref", f"#{self.metadata['book_uri']}")
            title.text = self.metadata['book']

            author = teiHeader.find(".//tei:titleStmt/tei:author", NS)
            author.set("ref", f"#{self.metadata['auth_uri']}")
            author.text = self.metadata['author']

            bibl = teiHeader.find(".//tei:sourceDesc/tei:bibl", NS)
            ptr = etree.SubElement(bibl, "ptr")
            ptr.set("target", f"#{self.metadata['book_uri']}")
        
        # Preserve non-machine readable data as xenodata
        if self.md.simple_metadata:
            xenoData = etree.Element("xenoData")
            xenoData.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            xenoString = "\n"
            for metadata in self.md.simple_metadata:
                xenoString += str(metadata) + "\n"
            xenoData.text = xenoString 
            teiHeader.append(xenoData)

        # If there are page numbers, the first one needs to be placed at the beginning
        # of the document because TEI marks page beginnings, not endings.
        pb = self._pagenum_lookdown(0)
        if pb:
            self._create_pb(pb)

        # Process content
        for pos, content in enumerate(self.md.content):
            self._convertStructure(content, pos)
        

    def _convertStructure(self, content, pos):
        """Convert an oimdp.Content object to a TEI element"""

        PARALIKE = [f"{TEINS}p", f"{TEINS}ab", f"{TEINS}entryFree", f"{TEINS}lg"]

        def _set_closest_container():
            """ set the context node to closest div or body """
            if self.context_node.tag != f"{TEINS}body":
                # Locate closest div
                closest = self.context_node.xpath("ancestor::tei:div[not(@type)]", namespaces=NS)

                if len(closest):
                    self.context_node = closest[-1]
                else:
                    # Return to body
                    self.context_node = self.body

        def _set_closest_container_for_paralike():
            """ set the context node to closest usable div. """

            def _create(ctx):
                div = etree.SubElement(ctx, f"{TEINS}div")
                self.context_node = div

            if self.context_node.tag == f"{TEINS}div":
                children = self.context_node.getchildren()
                # Paragraph-like elements must not be preceded by divs.
                if len(children) and children[-1].tag == f"{TEINS}div":
                    _create(self.context_node)

            else:                
                # Locate closest div like structure
                closest = self.context_node.xpath("ancestor::tei:div", namespaces=NS)

                if len(closest):
                    children = closest[-1].getchildren()
                    # Paragraph-like elements must not be preceded by divs.
                    if len(children) and children[-1].tag != f"{TEINS}div":
                        self.context_node = closest[-1]
                    else:
                        _create(self.body)
                else:
                    _create(self.body)

        def _create_p(tag="p", attributes={}):
            _set_closest_container_for_paralike()
            el = etree.SubElement(self.context_node, f"{TEINS}{tag}")
            if attributes:
                for att in attributes:
                    el.set(att, attributes[att]) 
            self.context_node = el

        # Riwāyāt
        if isinstance(content, Riwayat):
            _create_p(tag="ab", attributes={"type": "rwy"})

        elif isinstance(content, Paragraph):
            _create_p()

        elif isinstance(content, PageNumber):
            # PageNumber typically marks the end of a page, while TEI marks the beginning.
            # We need to do a look-up to move the page to the right location.
            next_pagenum = self._pagenum_lookdown(pos + 1)
            if next_pagenum:
                self._create_pb(next_pagenum)

        elif isinstance(content, Verse):
            if self.context_node.tag != f"{TEINS}lg":
                _set_closest_container_for_paralike()
                self.context_node = etree.SubElement(self.context_node, f"{TEINS}lg")
            
            self.context_node = etree.SubElement(self.context_node, f"{TEINS}l")

            if len(content.parts) > 0:
                for part in content.parts:
                    self._convertPart(part, pos)
                self._appendText(self.context_node, "\n")
            self.context_node = self.context_node.getparent()

        elif isinstance(content, Line):
            addlinebreak = True
            # Lines after certain structure markers are headers
            prev = self.md.content[pos - 1]
            if (
                isinstance(prev, BioOrEvent) or 
                isinstance(prev, DictionaryUnit) or
                isinstance(prev, DoxographicalItem)
            ) and self.context_node.tag == f"{TEINS}div":
                self.context_node = etree.SubElement(self.context_node, f"{TEINS}head")
                addlinebreak = False
            else:
                if self.context_node.tag not in PARALIKE:
                    _create_p()
                etree.SubElement(self.context_node, f"{TEINS}lb")

            # Process line parts
            if len(content.parts) > 0:
                for part in content.parts:
                    self._convertPart(part, pos)

            if addlinebreak:
                self._appendText(self.context_node, "\n")                

        elif isinstance(content, SectionHeader):
            # make sure this isn't used as a closing tag to resume content in the previous div.
            # (no value or empty string value)
            # Removing this temporarily since this behavior seems to be implemented inconsistently.
            # val = content.value or ""
            # if "".join(val.split()) == "":
            #     closest = self.context_node.xpath("ancestor::tei:div[not(@type)] | ancestor::tei:body", namespaces=NS)
            #     if len(closest):
            #         if self.context_node.tag == f"{TEINS}div":
            #             self.context_node = closest[-1]
            #         else:
            #             self.context_node = closest[-2]
            #     return
            
            # make sure we are in a section (untyped) div ...
            if self.context_node.tag != f"{TEINS}div" or self.context_node.get("type"):
                # ... or find the closest ...
                closest = self.context_node.xpath("ancestor::tei:div[not(@type)] | ancestor::tei:body", namespaces=NS)
                if len(closest):
                    self.context_node = closest[-1]
                else:
                    # ... or create it.
                    self.context_node = etree.SubElement(self.context_node, f"{TEINS}div")
            
            # Check level
            cur_level = len(self.context_node.xpath("ancestor-or-self::tei:div[not(@type)]", namespaces=NS))
            level_diff = content.level - cur_level

            def _is_viable(container):
                """  check that the <div> is either empty or only contains lb, pb, or head """
                allowed_children = [f"{TEINS}lb", f"{TEINS}pb", f"{TEINS}head"]
                children = container.getchildren()
                if len(children):
                    for child in children:
                        if child.tag not in allowed_children:
                            return False
                return True

            if level_diff == 0 and not _is_viable(self.context_node):
                # Check viability or step up up a level and create new div
                _set_closest_container()
                self.context_node = etree.SubElement(self.context_node, f"{TEINS}div")
            elif level_diff > 0:
                # Needs nesting.
                for step in range(level_diff):
                    self.context_node = etree.SubElement(self.context_node, f"{TEINS}div")
            else:
                # Needs to step out by the level difference.
                # try: 
                ancestors = self.context_node.xpath("ancestor::tei:div[not(@type)]", namespaces=NS)
                if len(ancestors):
                    ancestor = ancestors[level_diff]
                    if ancestor is not None:
                        self.context_node = ancestor
                        if not _is_viable(ancestor):
                            _set_closest_container()
                            self.context_node = etree.SubElement(self.context_node, f"{TEINS}div")

            head = etree.SubElement(self.context_node, f"{TEINS}head")
            head.text = content.value.strip()

        # elif isinstance(content, AdministrativeRegion):
            #TODO IN PARSER!
            
        elif isinstance(content, BioOrEvent):
            _set_closest_container()
                
            div = etree.SubElement(self.context_node, f"{TEINS}div")

            if content.be_type == "wom":
                div.set("type", "biography")
                div.set("subtype", "woman")
            elif content.be_type == "man":
                div.set("type", "biography")
                div.set("subtype", "man")                
            elif content.be_type == "ref":
                div.set("type", "biography")
                div.set("subtype", "ref_or_rep")
            elif content.be_type == "names":
                div.set("type", "names")
            elif content.be_type == "event":
                div.set("type", "event")
            elif content.be_type == "events":
                div.set("type", "events")
        
            self.context_node = div

        elif isinstance(content, DictionaryUnit):
            _set_closest_container_for_paralike()
                
            ef = etree.SubElement(self.context_node, f"{TEINS}entryFree")

            if content.dic_type == "bib":
                ef.set("type", "bib")
            elif content.dic_type == "lex":
                ef.set("type", "lex")
            elif content.dic_type == "nis":
                ef.set("type", "nis")
            elif content.dic_type == "top":
                ef.set("type", "top")
        
            self.context_node = ef
        elif isinstance(content, DoxographicalItem):
            _set_closest_container()

            div = etree.SubElement(self.context_node, f"{TEINS}div")
            div.set("type", "doxographical")

            if content.dox_type == "pos":
                div.set("subtype", "pos")
            elif content.dox_type == "sec":
                div.set("subtype", "sec")

            self.context_node = div
        elif isinstance(content, Editorial):
            _set_closest_container()

            div = etree.SubElement(self.context_node, f"{TEINS}div")
            div.set("type", "editorial")

            self.context_node = div

    def _convertPart(self, content, cur_pos):
        """ Convert line parts """ 
        if isinstance(content, Isnad) or isinstance(content, Matn) or isinstance(content, Hukm):
            parts = {
                "Isnad": "isn",
                "Matn": "matn",
                "Hukm": "hukm",
            }

            if self.context_node.tag != f"{TEINS}ab":
                raise Exception("Riwāyāt part not in Riwāyāt")
            
            seg = etree.SubElement(self.context_node, f"{TEINS}seg")
            part_type = parts.get(type(content).__name__)
            seg.set("type", part_type)
            
            self.context_linepart = seg

        elif isinstance(content, Hemistich):
            if self.context_node.tag != f"{TEINS}l":
                raise Exception("Hemistic outside of Verse structure")
            else:
                c = etree.SubElement(self.context_node, f"{TEINS}caesura")
                c.tail = " "

        elif isinstance(content, Milestone):
            milestone = etree.SubElement(self.context_node, f"{TEINS}milestone")
            milestone.set("n", "300")
            milestone.set("unit", "words")
            
        elif isinstance(content, Date):
            date = etree.SubElement(self.context_node, f"{TEINS}date")
            date.set("type", content.date_type)
            date.set("calendar", "#ah")
            date.set("when-custom", content.value)
            date.tail = " "
        elif isinstance(content, Age):
            num = etree.SubElement(self.context_node, f"{TEINS}num")
            num.set("type", "age")
            num.set("value", content.value)
            num.tail = " "
        elif isinstance(content, NamedEntity):
            self._appendText(self.context_node, " ")
            text_to_add = content.text
            if content.prefix > 0:
                pre = content.text[:content.prefix]
                self._appendText(self.context_node, pre)
                text_to_add = content.text[content.prefix:]
            if content.ne_type == "soc":
                seg = etree.SubElement(self.context_node, f"{TEINS}seg")
                seg.set("type", "biochar")
                seg.text = text_to_add
                seg.tail = " "
            elif content.ne_type == "top":
                pn = etree.SubElement(self.context_node, f"{TEINS}placeName")
                pn.text = text_to_add
                pn.tail = " "
            elif content.ne_type == "per":
                pn = etree.SubElement(self.context_node, f"{TEINS}persName")
                pn.text = text_to_add
                pn.tail = " "
            elif content.ne_type == "src":
                pn = etree.SubElement(self.context_node, f"{TEINS}persName")
                pn.set("role", "source")
                pn.text = text_to_add
                pn.tail = " "

        elif isinstance(content, TextPart):
            node = self.context_node
            if self.context_linepart is not None:
                node = self.context_linepart

            self._appendText(node, content.orig.strip())

        elif isinstance(content, PageNumber):
            # PageNumber typically marks the end of a page, while TEI marks the beginning.
            # We need to do a look-up to move the page to the right location.
            next_pagenum = self._pagenum_lookdown(cur_pos + 1)
            if next_pagenum:
                self._create_pb(next_pagenum)

        else:
            self.context_linepart = None