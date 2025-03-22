from pages import *

class PageScript:
    def __init__(self):
        self.current_page = None

    def change_page(self, page):
        if self.current_page != page:
            self.destroy_page()
            self.pack_page(page)
        else: 
            print("Page already packed")

    def get_current_page(self):
        return self.current_page
    
    def destroy_page(self):
        self.current_page.destroy()

    def pack_page(self, page):
        self.current_page = page
        page.pack(fill="both", expand=True)