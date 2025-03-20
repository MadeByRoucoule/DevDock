from pages import *

class PageScript:
    def __init__(self):
        self.current_page = None

    def change_page(self, page):
        self.pack_page(page)

    def get_current_page(self):
        return self.current_page
    
    def unpack_page(self):
        self.current_page.pack_forget()

    def pack_page(self, page):
        self.current_page = page
        page.pack(fill="both", expand=True)