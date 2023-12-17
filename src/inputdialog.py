from PyQt5.QtCore import Qt
from pathlib import Path

from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QGridLayout,
    QVBoxLayout,
    QPushButton,
    QCheckBox,
    QDialog,
    QFrame,
    QLabel
)


class InputDialog:
    dialog: QDialog
    out: list[Path]
    _fields: dict[Path, QCheckBox]

    def __init__(self, files: list[Path]):
        self.dialog = QDialog(None)
        self.dialog.setWindowTitle("Running Backup")
        self.dialog.setMinimumWidth(300)
        # set defaults
        self.out = list()
        self.dialog.setStyleSheet("QDialog {background-color: #202328;}\n"
                                  "QWidget {font-size: 11pt;}")
        self._fields = dict()
        # construct widgets
        top_layout = QVBoxLayout(self.dialog)
        top_label = QLabel(self.dialog)
        top_label.setText("Select archives to update:")
        top_layout.addWidget(top_label)
        # add subbox
        frame = QFrame(self.dialog)
        frame.setStyleSheet("QFrame {background-color: #2d3640;}\n"
                            "QPushButton {min-width: 80px;}")
        top_layout.addWidget(frame)
        main_layout = QGridLayout(frame)
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(2, 1)
        # populate subbox
        for i, file in enumerate(files):
            lbl = QLabel(frame)
            lbl.setText(file.stem)
            main_layout.addWidget(lbl, i, 0, Qt.AlignRight)
            chkBox = QCheckBox(frame)
            chkBox.setChecked(True)
            main_layout.addWidget(chkBox, i, 1)
            self._fields.update({file: chkBox})
        # add subbox btns
        layout_btns = QVBoxLayout()
        layout_btns.setContentsMargins(10, 0, 0, 0)
        main_layout.addLayout(layout_btns, 0, 2, len(files), 1)
        btn_check_all = QPushButton(frame)
        btn_check_all.setText("Select all")
        btn_check_all.clicked.connect(self._checkAll)
        layout_btns.addWidget(btn_check_all)
        layout_btns.setAlignment(btn_check_all, Qt.AlignLeft)
        btn_check_none = QPushButton(frame)
        btn_check_none.setText("Deselect all")
        btn_check_none.clicked.connect(self._checkNone)
        layout_btns.addWidget(btn_check_none)
        layout_btns.setAlignment(btn_check_none, Qt.AlignLeft)
        # construct buttonbox
        btnbox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btnbox.accepted.connect(self._submit)
        btnbox.rejected.connect(self.dialog.close)
        btnbox.setCenterButtons(True)
        top_layout.addWidget(btnbox)
        # run
        self.dialog.exec()

    def _checkAll(self):
        for cbx in self._fields.values():
            cbx.setChecked(True)

    def _checkNone(self):
        for cbx in self._fields.values():
            cbx.setChecked(False)

    def _submit(self):
        for pth, cbx in self._fields.items():
            if cbx.isChecked():
                self.out.append(pth)
        self.dialog.close()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    from sys import argv
    
    app = QApplication(argv)
    files = list(Path(__file__).parent.iterdir())
    ans = InputDialog(files).out
    print(ans)
