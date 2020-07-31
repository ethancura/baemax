# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'triage.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox 
#from triageResultUI import Ui_triageResult
import numpy as np
import csv
from keras_nn import model
from datetime import datetime

class Ui_triageInterface(object):
    #grab inputs from UI
    def button_click(self):
        #patient Name
        firstName = self.patientFirstNameLineEdit.text()
        lastName = self.patientLastNameLineEdit.text()

        #patient Sex
        isMale = self.maleRadioButton.isChecked()
        isFemale = self.radioButton.isChecked()
        if(isMale):
            gender = 0
        if(isFemale):
            gender = 1

        #patient Age
        DOB = self.DOBQDateEdit.date()
        DOBString = DOB.toString(self.DOBQDateEdit.displayFormat())
        DOBStringSplit = DOBString.split("/")
        DOBMonth = int(DOBStringSplit[0])
        DOBYear = int(DOBStringSplit[2])
        DOBDate = int(DOBStringSplit[1])
        CurrentDate = str(datetime.date(datetime.now()))
        CurrentDateSplit = CurrentDate.split("-")
        CurrentDateMonth = int(CurrentDateSplit[1])
        CurrentDateYear = int(CurrentDateSplit[0])
        CurrentDateDate = int(CurrentDateSplit[2])
        age = CurrentDateYear - DOBYear
        if(CurrentDateMonth < DOBMonth): age = age - 1
        if(CurrentDateMonth == DOBMonth):
            if(CurrentDateDate < DOBDate): age = age - 1
        
        #patient Reason for Visit
        visitInput = self.reasonForVisitComboBox.currentText()
        if(visitInput == "Stomach or abdominal pain, cramps, or spasms"):
            visitReason1 = 1
        else:
            visitReason1 = 0
        if(visitInput == "Chest pain and related symptoms"):
            visitReason2 = 1
        else:
            visitReason2 = 0
        if(visitInput == "Fever"):
            visitReason3 = 1
        else:
            visitReason3 = 0
        if(visitInput == "Cough"):
            visitReason4 = 1
        else:
            visitReason4 = 0
        if(visitInput == "Shortness of breath"):
            visitReason5 = 1
        else:
            visitReason5 = 0
        if(visitInput == "Pain at specified site"):
            visitReason6 = 1
        else:
            visitReason6 = 0
        if(visitInput == "Headache, pain in head"):
            visitReason7 = 1
        else:
            visitReason7 = 0
        if(visitInput == "Back pain"):
            visitReason8 = 1
        else:
            visitReason8 = 0
        if(visitInput == "Vomiting"):
            visitReason9 = 1
        else:
            visitReason9 = 0
        if(visitInput == "Symptoms referable to throat"):
            visitReason10 = 1
        else:
            visitReason10 = 0
        if(visitInput == "Other reasons"):
            visitReason11 = 1
        else:
            visitReason11 = 0

        #patient mode of transportation
        isAmbulance = self.radioButton_2.isChecked()
        isOther = self.radioButton_3.isChecked()
        if(isAmbulance):
            transport = 1
        if(isOther):
            transport = 0

        #vitals blood pressure
        bpInput = self.comboBox.currentText()
        if(bpInput == "Not High"):
            bp0 = 1
        else:
            bp0 = 0
        if(bpInput == "Prehypertension"):
            bp1 = 1
        else:
            bp1 = 0
        if(bpInput == "Stage 1 hypertension"):
            bp2 = 1
        else:
            bp2 = 0
        if(bpInput == "Stage 2 hypertension"):
            bp3 = 1
        else:
            bp3 = 0

        #vitals pulse oximetry
        pulseOximetry = float(self.pulseOxLineEdit.text())
        if(pulseOximetry >= 95 and pulseOximetry <= 100):
            pOx = 0
        else:
            pOx = 1

        #vitals temperature
        temp = float(self.tempLineEdit.text())
        
        #vitals heart rate
        hRate = float(self.heartLineEdit.text())

        #vitals respiratory rate
        rRate = float(self.respLineEdit.text())

        #write inputs to file (write twice to avoid code complications)
        with open('tlcsv.csv', 'w', newline='') as f:
            thewriter = csv.writer(f)
            thewriter.writerow([gender,46,
                                visitReason1,visitReason2,visitReason3,visitReason4,visitReason5,visitReason6,visitReason7,visitReason8,visitReason9,visitReason10,visitReason11,
                                transport,
                                bp0,bp1,bp2,bp3,pOx,temp,hRate,rRate])
            thewriter.writerow([gender,46,
                                visitReason1,visitReason2,visitReason3,visitReason4,visitReason5,visitReason6,visitReason7,visitReason8,visitReason9,visitReason10,visitReason11,
                                transport,
                                bp0,bp1,bp2,bp3,pOx,temp,hRate,rRate])

        #calculate output using keras_nn
        xnew = np.loadtxt('tlcsv.csv', delimiter=',')
        pred = xnew[:,0:22]
        ynew = model.predict(pred) #the NN model
        first = ynew[0,:] #grab only list 1
        indx = np.argmax(first) #get max num in array and print out index
        tl=indx+1 #triage level

        #output to results file

        #to see output from the interface onto terminal (delete later)
        print(firstName, lastName)
        print("sex:", gender)
        print("dob:", DOBString)
        print("age:", age)
        print("reason for visit:", visitInput)
        print(visitReason1, visitReason2, visitReason3, visitReason4, visitReason5, visitReason6, visitReason7, visitReason8, visitReason9, visitReason10, visitReason11)
        print("mode of transport:", transport)
        print("blood pressure:", bpInput)
        print(bp0, bp1, bp2, bp3)
        print("pulse oximetry:", pulseOximetry, pOx)
        print("temperature:", temp)
        print("heart rate:", hRate)
        print("respiratory rate:", rRate)
        print("predicted triage level:", tl)
        print("\n")

        #place output to result interface
        if(tl == 1): tMessage = "1 - Needs Immediate Lifesaving Intervention"
        if(tl == 2): tMessage = "2 - High Risk"
        if(tl == 3): tMessage = "3 - Two or more Resources"
        if(tl == 4): tMessage = "4 - One or more Resources"
        if(tl == 5): tMessage = "5 - No Resources"
        msg = QMessageBox()
        msg.setWindowTitle('eTriage Result')
        msg.setText("The predicted triage level for patient " + firstName + " " + lastName + ": \n" + tMessage)
        x = msg.exec_()
        
    def setupUi(self, triageInterface):
        triageInterface.setObjectName("triageInterface")
        triageInterface.resize(952, 421)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setUnderline(False)
        triageInterface.setFont(font)
        self.label = QtWidgets.QLabel(triageInterface)
        self.label.setGeometry(QtCore.QRect(10, 50, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(triageInterface)
        self.label_2.setGeometry(QtCore.QRect(400, 50, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(triageInterface)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.DOBQDateEdit = QtWidgets.QDateEdit(triageInterface)
        self.DOBQDateEdit.setGeometry(QtCore.QRect(10, 150, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.DOBQDateEdit.setFont(font)
        self.DOBQDateEdit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.DOBQDateEdit.setObjectName("DOBQDateEdit")
        self.label_5 = QtWidgets.QLabel(triageInterface)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 71, 16))
        self.label_5.setObjectName("label_5")
        self.patientLastNameLineEdit = QtWidgets.QLineEdit(triageInterface)
        self.patientLastNameLineEdit.setGeometry(QtCore.QRect(400, 70, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.patientLastNameLineEdit.setFont(font)
        self.patientLastNameLineEdit.setObjectName("patientLastNameLineEdit")
        self.patientFirstNameLineEdit = QtWidgets.QLineEdit(triageInterface)
        self.patientFirstNameLineEdit.setGeometry(QtCore.QRect(10, 70, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.patientFirstNameLineEdit.setFont(font)
        self.patientFirstNameLineEdit.setObjectName("patientFirstNameLineEdit")
        self.reasonForVisitComboBox = QtWidgets.QComboBox(triageInterface)
        self.reasonForVisitComboBox.setGeometry(QtCore.QRect(240, 150, 541, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.reasonForVisitComboBox.setFont(font)
        self.reasonForVisitComboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.reasonForVisitComboBox.setObjectName("reasonForVisitComboBox")

        #adding reasons to combo box
        self.reasonForVisitComboBox.addItem("select")
        self.reasonForVisitComboBox.addItem("Stomach or abdominal pain, cramps, or spasms")
        self.reasonForVisitComboBox.addItem("Chest pain and related symptoms")
        self.reasonForVisitComboBox.addItem("Fever")
        self.reasonForVisitComboBox.addItem("Cough")
        self.reasonForVisitComboBox.addItem("Shortness of breath")
        self.reasonForVisitComboBox.addItem("Pain at specified site")
        self.reasonForVisitComboBox.addItem("Headache, pain in head")
        self.reasonForVisitComboBox.addItem("Back symptoms")
        self.reasonForVisitComboBox.addItem("Vomiting")
        self.reasonForVisitComboBox.addItem("Symptoms referable to throat")
        self.reasonForVisitComboBox.addItem("Other reasons")

        self.label_6 = QtWidgets.QLabel(triageInterface)
        self.label_6.setGeometry(QtCore.QRect(240, 130, 91, 16))
        self.label_6.setObjectName("label_6")
        self.sexGroupBox = QtWidgets.QGroupBox(triageInterface)
        self.sexGroupBox.setGeometry(QtCore.QRect(810, 50, 120, 71))
        self.sexGroupBox.setObjectName("sexGroupBox")
        self.maleRadioButton = QtWidgets.QRadioButton(self.sexGroupBox)
        self.maleRadioButton.setGeometry(QtCore.QRect(10, 20, 82, 17))
        self.maleRadioButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.maleRadioButton.setObjectName("maleRadioButton")
        self.radioButton = QtWidgets.QRadioButton(self.sexGroupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 40, 82, 17))
        self.radioButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.radioButton.setObjectName("radioButton") #female radio button
        self.groupBox_2 = QtWidgets.QGroupBox(triageInterface)
        self.groupBox_2.setGeometry(QtCore.QRect(800, 130, 131, 71))
        self.groupBox_2.setObjectName("groupBox_2")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 20, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_3.setGeometry(QtCore.QRect(10, 40, 82, 17))
        self.radioButton_3.setObjectName("radioButton_3")
        self.label_4 = QtWidgets.QLabel(triageInterface)
        self.label_4.setGeometry(QtCore.QRect(10, 230, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(triageInterface)
        self.label_7.setGeometry(QtCore.QRect(10, 260, 111, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(triageInterface)
        self.label_8.setGeometry(QtCore.QRect(280, 260, 101, 16))
        self.label_8.setObjectName("label_8")
        self.pulseOxLineEdit = QtWidgets.QLineEdit(triageInterface)
        self.pulseOxLineEdit.setGeometry(QtCore.QRect(280, 280, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pulseOxLineEdit.setFont(font)
        self.pulseOxLineEdit.setObjectName("pulseOxLineEdit")
        self.tempLineEdit = QtWidgets.QLineEdit(triageInterface)
        self.tempLineEdit.setGeometry(QtCore.QRect(450, 280, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tempLineEdit.setFont(font)
        self.tempLineEdit.setObjectName("tempLineEdit")
        self.label_9 = QtWidgets.QLabel(triageInterface)
        self.label_9.setGeometry(QtCore.QRect(450, 260, 151, 16))
        self.label_9.setObjectName("label_9")
        self.heartLineEdit = QtWidgets.QLineEdit(triageInterface)
        self.heartLineEdit.setGeometry(QtCore.QRect(620, 280, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.heartLineEdit.setFont(font)
        self.heartLineEdit.setObjectName("heartLineEdit")
        self.respLineEdit = QtWidgets.QLineEdit(triageInterface)
        self.respLineEdit.setGeometry(QtCore.QRect(790, 280, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.respLineEdit.setFont(font)
        self.respLineEdit.setObjectName("respLineEdit")
        self.label_10 = QtWidgets.QLabel(triageInterface)
        self.label_10.setGeometry(QtCore.QRect(620, 260, 121, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(triageInterface)
        self.label_11.setGeometry(QtCore.QRect(790, 260, 121, 16))
        self.label_11.setObjectName("label_11")
        self.comboBox = QtWidgets.QComboBox(triageInterface)
        self.comboBox.setGeometry(QtCore.QRect(10, 280, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox") #blood pressure
        
        self.comboBox.addItem("select")
        self.comboBox.addItem("Not High")
        self.comboBox.addItem("Prehypertension")
        self.comboBox.addItem("Stage 1 hypertension")
        self.comboBox.addItem("Stage 2 hypertension")

        self.pushButton = QtWidgets.QPushButton(triageInterface)
        self.pushButton.setGeometry(QtCore.QRect(810, 370, 101, 31))
        self.pushButton.setObjectName("pushButton") #calculateButton

        #self.pushButton.clicked.connect(self.openWindow) #open results window (delete)
        self.pushButton.clicked.connect(self.button_click) #grab inputs

        self.retranslateUi(triageInterface)
        QtCore.QMetaObject.connectSlotsByName(triageInterface)
        triageInterface.setTabOrder(self.patientFirstNameLineEdit, self.patientLastNameLineEdit)
        triageInterface.setTabOrder(self.patientLastNameLineEdit, self.maleRadioButton)
        triageInterface.setTabOrder(self.maleRadioButton, self.radioButton)
        triageInterface.setTabOrder(self.radioButton, self.DOBQDateEdit)
        triageInterface.setTabOrder(self.DOBQDateEdit, self.reasonForVisitComboBox)
        triageInterface.setTabOrder(self.reasonForVisitComboBox, self.radioButton_2)
        triageInterface.setTabOrder(self.radioButton_2, self.radioButton_3)
        triageInterface.setTabOrder(self.radioButton_3, self.comboBox)
        triageInterface.setTabOrder(self.comboBox, self.pulseOxLineEdit)
        triageInterface.setTabOrder(self.pulseOxLineEdit, self.tempLineEdit)
        triageInterface.setTabOrder(self.tempLineEdit, self.heartLineEdit)
        triageInterface.setTabOrder(self.heartLineEdit, self.respLineEdit)
        triageInterface.setTabOrder(self.respLineEdit, self.pushButton)

    def retranslateUi(self, triageInterface):
        _translate = QtCore.QCoreApplication.translate
        triageInterface.setWindowTitle(_translate("triageInterface", "eTriage"))
        self.label.setText(_translate("triageInterface", "First Name"))
        self.label_2.setText(_translate("triageInterface", "Last Name"))
        self.label_3.setText(_translate("triageInterface", "Patient Information"))
        self.label_5.setText(_translate("triageInterface", "Date of Birth"))
        self.label_6.setText(_translate("triageInterface", "Reason for Visit"))
        self.sexGroupBox.setTitle(_translate("triageInterface", "Sex"))
        self.maleRadioButton.setText(_translate("triageInterface", "Male"))
        self.radioButton.setText(_translate("triageInterface", "Female"))
        self.groupBox_2.setTitle(_translate("triageInterface", "Mode of Transportation"))
        self.radioButton_2.setText(_translate("triageInterface", "Ambulance"))
        self.radioButton_3.setText(_translate("triageInterface", "Other"))
        self.label_4.setText(_translate("triageInterface", "Patient Vitals"))
        self.label_7.setText(_translate("triageInterface", "Blood Pressure (mmHg)"))
        self.label_8.setText(_translate("triageInterface", "Pulse Oximetry (%)"))
        self.label_9.setText(_translate("triageInterface", "Temperature (°F)"))
        self.label_10.setText(_translate("triageInterface", "Heart Rate (bpm)"))
        self.label_11.setText(_translate("triageInterface", "Respiratory Rate (bpm)"))
        self.pushButton.setText(_translate("triageInterface", "Calculate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.jpg'))
    triageInterface = QtWidgets.QDialog()
    ui = Ui_triageInterface()
    ui.setupUi(triageInterface)
    triageInterface.show()
    sys.exit(app.exec_())

