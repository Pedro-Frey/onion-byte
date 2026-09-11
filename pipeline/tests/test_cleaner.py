from pipeline.cleaner import DataCleaner

def test_remove_html_tags():
    html = "<p>Test <b>bold</b></p>"
    assert DataCleaner.remove_html_tags(html) == "Test bold"

def test_clean_dict():
    data = {"name": "<b>João</b>   Silva", "nested": {"field": "<script>alert(1)</script>texto"}}
    cleaned = DataCleaner.clean_dict(data)
    assert cleaned["name"] == "João Silva"
    assert cleaned["nested"]["field"] == "texto"
