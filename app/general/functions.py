from lxml import html as html_module
def crop_text(text, max_length):
    """
    Crop the text to a maximum length without breaking words.
    If the max_length falls in the middle of a word, it crops to the end of the previous word.
    """
    if len(text) <= max_length:
        return text
    else:
        # Find the last space within the allowed length
        last_space = text.rfind(' ', 0, max_length)
        return text[:last_space] if last_space != -1 else text[:max_length]

def html_2_text(html_content):
    tree = html_module.fromstring(html_content)
    # text_list = tree.xpath('//text()')
    # text_list = tree.xpath('//text()[not(ancestor::script)]')
    text_list = tree.xpath('//text()[not(ancestor::script) and normalize-space()]')
    text_list = [text.strip() for text in text_list]
    return "\n".join(text for text in text_list if text!="")