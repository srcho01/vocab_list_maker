import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from make_file import *

# Connect UI
form_class = uic.loadUiType("ui.ui")[0]

class Window(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        ### handler ###  
        # file input
        self.drag_and_drop.dragEnterEvent = self.dragEnterEvent
        self.drag_and_drop.dropEvent = self.dropEvent
        self.drag_and_drop.clicked.connect(self.selectFile)
        
        # file delete
        self.file_list.customContextMenuRequested.connect(self.showContextMenu)
        
        # make file
        self.make.clicked.connect(self.prepare_file)
    
    ### add file with duplicate check
    def add_file(self, files):
        for f in files:
            # 이미 있는 파일인지 확인
            for index in range(self.file_list.count()):
                existing_item = self.file_list.item(index)
                if existing_item.text() == f:
                    return
            
            # 파일이 중복되지 않는 경우에만 추가
            list_item = QListWidgetItem(f)
            self.file_list.addItem(list_item)
    
    ### file drag and drop function
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_names = [url.toLocalFile() for url in event.mimeData().urls() if url.toLocalFile().endswith('.txt')]
        self.add_file(file_names)

    ### file select
    def selectFile(self):
        # 파일 선택 대화 상자 띄우기
        file_names, _ = QFileDialog.getOpenFileNames(self, 'Select Files', filter="Text files (*.txt)")
        if file_names:
            # 선택된 파일 목록을 파일 목록 위젯에 추가
            self.add_file(file_names)
        
    ### file delete
    def showContextMenu(self, pos):
        # 컨텍스트 메뉴 생성
        menu = QMenu(self)
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.deleteSelected)
        menu.addAction(delete_action)

        # 컨텍스트 메뉴 표시
        menu.exec_(self.file_list.mapToGlobal(pos))

    def deleteSelected(self):
        # 선택된 항목 삭제
        selected_items = self.file_list.selectedItems()
        for item in selected_items:
            self.file_list.takeItem(self.file_list.row(item))
    
    ### prepare file            
    def prepare_file(self):
        # 파일 저장 대화상자 띄우기
        save_path = QFileDialog.getExistingDirectory(self, '저장 경로', '')
        if not save_path: return
        
        files = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            files.append(item.text())
        
        is_numbering = self.check_numbering.isChecked()
        is_shuffle = self.check_shuffle.isChecked()
        is_foreign = self.check_foreign.isChecked()
        is_korean = self.check_korean.isChecked()
        is_answer = self.check_answer.isChecked()
        form = 'txt' if self.text.isChecked() else 'jpg'
        
        make_file(files, save_path, form, is_numbering, is_shuffle, is_foreign, is_korean, is_answer)
        
        self.file_list.clear()
    
if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = Window()
    myWindow.show()
    sys.exit(app.exec_())