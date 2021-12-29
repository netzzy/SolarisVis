﻿import re
import os
from dataclasses import dataclass
from typing import Any
import glob
import time
import fnmatch

from QClass import QClass
from CuryCueConnector import CuryCueConnector
from MysqlBase import MysqlBase
from UtilsClass import UtilsClass, IOP, IPAR
from InTableEditBase import *
from CuryCueStructsDef import *
from CuryCueAddByDragAndDrop import *
from FixtureUtils import *


class CuryCueClass (CuryCueStructsDef, MysqlBase, CuryCueConnector, UtilsClass, InTableDataEdit, CuryCueAddByDragAndDrop, FixtureUtils):
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        self.chopExportDisabled=False
        op.DP.PrintAndDisplay("{} init".format(ownerComp.name))
        MysqlBase.__init__(self, ownerComp)
        self.ConnectDb()
        self.LocalCueData = []
        self.LocalCueDataByID = dict()
        self.LocalFixtureData = []
        self.LocalFixturesByPath = dict()
        self.ActiveFields = []
        self.ActiveFieldsByPath = []
        self.lastActiveCompInUI=dict()
        self.lastAddedFixtureIndex=0
        self.CueEditMode=""
        CuryCueConnector.__init__(self)
        UtilsClass.__init__(self)
        InTableDataEdit.__init__(self)
        self.I = IOP(self)
        self.P = IPAR(self)

        self.UpdateFromDb()
        self.q = QClass(ownerComp)
        self.SKIPCUE=False
        print ("OK")
        run("op('{}').SetInitCue({})".format(
            self.ownerComp.path, 1), delayFrames=20)
        self.ExportMode=2
        
        pass

    # ИЗМЕНЕНИЕ КЛЮЧА 
    def Storeselected(self, updateDbAfter=True):
        res=None
        myFields = ['id_cue', 'id_fixture', 'par_name',
                    'par_value', 'fade_in', 'delay_in']
        if self.CurrentCueID > 0:
            i = 0
            for (id_fixture, par_value, path, par_name, fade, delay) in self.I.storedat.rows():
                if i > 0:
                    try:
                        par_value=float(par_value)
                        myFields[3]='par_value'
                    except: 
                        par_value=str(par_value)
                        myFields[3]='par_text_value'
                    newInsertQuery = self.QUERY_INSERT(table="cue_float_data", fields=myFields,
                                                       fieldsData=[int(self.CurrentCueID), int(id_fixture), str(par_name), par_value, float(fade), float(delay)], conditionData=[])
                    res = self.insertIntoTable(newInsertQuery)
                    
                i += 1
            ui.status="{} {} {} в ключ \"{}\" ({})".format("Изменен или добавлен" if i==0 else "Изменено или добавлено", i, "параметр" if i==1 else "параметра", self.Curcuename, self.Curcueid)
            if updateDbAfter:
                self.UpdateFromDb()
                self.SetInitCue(1)
            return res
        else:
            ui.status="No Q selected"
        
        pass

    def Process_InputRealtimeVal(self, v1, v2):
        if op(v1) is not None:
            if hasattr(op(v1).par, str(v2)):
                myPar=getattr(op(v1).par, str(v2))
                if myPar.isToggle:
                    if myPar.eval()==True:
                        v=1 
                    else:
                        v=0
                elif myPar.isString:
                    v=myPar.eval()
                else:
                    v="%g" % myPar.eval()
                return v

        

    def RunCue(self, cue, momentary=False):
        
        ui.status=("Running CUE: {}, name: {}".format(cue.id, cue.name))
        self.q.Forcestop()
        for i in range(0, len(self.ActiveFields)):
            # ПРОВЕРЯЕМ, ЕСТЬ ЛИ ТАКОЕ АКТИВНОЕ ПОЛЕ В ПАРАМЕТРАХ ВЫЗВАННОГО КЛЮЧА 
            if self.ActiveFields[i].full_par_path in cue.pars_float_by_path:
                # ЕСЛИ ЕСТЬ, ЗАПУСКАЕМ
                myCue = cue.pars_float_by_path[self.ActiveFields[i].full_par_path]
                # self.ActiveFields[i].par_value=myCue.par_value
                # ЕСЛИ ИЗМЕНИЛОСЬ ЗНАЧЕНИЕ В ПО ОТНОШЕНИЮ К АКТИВНОЙ ТАБЛИЦЕ ИЛИ ЕСЛИ ИЗМЕНИЛСЯ ТЕКСТ В ТЕКСТОВОМ ПОЛЕ - ЗАПУСКАЕМ ФЭЙДЕР
                if self.ActiveFields[i].par_value != myCue.par_value or (self.ActiveFields[i].par_text_value != myCue.par_text_value):
                    # ЗАПОЛНЯЕМ СТРУКТУРУ ДАННЫХ ДЛЯ ФЭЙДЕРА
                    myCueTask = self.q.Qtask(name=myCue.par_name, value_start=self.ActiveFields[i].par_value, value_target=myCue.par_value,
                                             value_text=myCue.par_text_value,
                                             fade=myCue.fade_in, delay=myCue.delay_in, 
                                             full_par_path=self.ActiveFields[i].full_par_path, callback=self.CallbackFromFader,
                                             callback_complete=self.CallbackFromFaderComplete)
                    # ЕСЛИ ОТКЛЮЧЕНЫ ФЭЙДЫ В ИНТЕРФЕЙСЕ ДЛЯ ОТЛАДКИ ИЛИ ЕСЛИ ВЫЗОВ ПРОИСХОДИТ ИЗ ИНИЦИАЛИЗАТОРА (ТОГДА НЕ ФЭЙДИМ)
                    if self.FadesMode=="off" or momentary:
                        myCueTask.fade=0

                    # остановить фэйд если такой уже идёт
                    self.q.StopByPathIndex(self.ActiveFields[i].full_par_path)
                    # ЗАПУСКАЕМ ФЭЙД-ВЫЧИСЛИТЕЛЬ
                    self.q.CreateEvaluator(myCueTask)
                    self.ActiveFields[i].is_fading = 1
                    self.ActiveFields[i].is_fadingDelay = 0

                # ЗАПОЛНЯЕМ ЗНАЧЕНИЕ В АКТИВНОЙ ТАБЛИЦЕ, КОТОРЫЕ МОГУТ БЫТЬ ЗАПОЛНЕНЫ СРАЗУ 
                self.ActiveFields[i].fade_in = myCue.fade_in
                self.ActiveFields[i].delay_in = myCue.delay_in
                self.ActiveFields[i].is_cue_exist = 0 if myCue.is_derived else 1
                self.ActiveFields[i].id_par = myCue.id
            else:
                # ЕСЛИ НЕТ, ТО НЕ ЗАПУСКАЕМ, НО ОТМЕЧАЕМ, ЧТО ТАКОГО КЛЮЧА НЕТ 
                self.ActiveFields[i].is_cue_exist = 0
                self.ActiveFields[i].id_cue = 0
                if self.ActiveFields[i].is_fading == 1:
                    self.ActiveFields[i].extra_export_frames = 1

                # self.ActiveFields[i].par_value=self.ActiveFields[i].fixture_par_ref.default_value

        pass

    def CallbackFromFader(self, task):
        # print ("name:{}, from: {}, to:{}, v:{}, progress:{}, path: {}".format(task.name,task.value_start,
        #  task.value_target, task.value, task.progress, task.full_par_path))
        myField = self.ActiveFieldsByPath[task.full_par_path]
        myField.par_value = task.value
        myField.par_text_value=task.value_text

        pass

    def CallbackFromFaderComplete(self, task):
        myField = self.ActiveFieldsByPath[task.full_par_path]
        myField.is_fading = 0
        task.running=0
        # print ("Evals: {}, {}".format(len(self.q.evaluators), self.q.evaluators[0].task.running))
        if len(self.q.evaluators)==0:
            ui.status="Cue done"
            if self.LocalCueDataByID[int(self.Curcueid)].linked==1:
                self.Gonextcue()

            #self.Gonextcue()
        pass


    def Gonextcue(self):
        self.Gocue()

    def Goprevcue(self):
        self.Gocue(dir="back")
        pass
    def Gocue(self, dir="forward"):

        myCueObj=self.LocalCueDataByID[int(self.Curcueid)]
        cur_cue_index=self.LocalCueData.index(myCueObj)
        next_cue_index=cur_cue_index+1 if dir=="forward" else cur_cue_index-1
        if not next_cue_index > len(self.LocalCueData)-1 and next_cue_index >=0:
            nextCue=self.LocalCueData[next_cue_index]
            if not self.SKIPCUE:
                self.RunCue(nextCue)
            self.SetOwnerPar('Cueid', nextCue.id)
            self.SetOwnerPar('Cuename', nextCue.name)
            self.SetOwnerPar('Cueorder', nextCue.order)
            op(self.ownerComp.par.Ui).UpdateCueLists(next_cue_index)
            
          

    def CueCopy(self, row, _withItems):
        
        row = int(row) - 1
        myCue=self.LocalCueData[row]
        
        
            # print("cue: {}, withpars: {}, row: {} ".format( myCue.name, _withItems, row))

        r=self.executeUpdateQuery("INSERT INTO cue (`order`, `name`, `memo`, `is_enabled`) VALUES (%s, %s, %s, 1)",
                            [myCue.order+0.1, myCue.name + "(new)", myCue.memo])
        r1=None
        if _withItems:
            for cuePar in myCue.pars_float:
                if cuePar.id != -1:
                    newCueId=r[1]
                    if newCueId > 0:
                        print ("id_cue:{}, id_fixture:{}, par_name:{}, par_value:{},par_value_text:{}, fade_in:{}, delay_in:{}".format(myCue.id, cuePar.id_fixture, 
                        cuePar.par_name, cuePar.par_value,cuePar.par_text_value,  cuePar.fade_in, cuePar.delay_in ))
                        r1=self.executeUpdateQuery("INSERT INTO cue_float_data (id_cue, id_fixture, par_name, par_value, par_text_value, fade_in, delay_in) VALUES (%s, %s, %s,%s, %s, %s, %s)",
                        [newCueId, cuePar.id_fixture, cuePar.par_name, cuePar.par_value, cuePar.par_text_value, cuePar.fade_in, cuePar.delay_in])
                        if not r1[0]:
                            ui.status="Ошибка копирования ключа {}, в параметре {}".format(myCue.id, cuePar.par_name)
                            self.UpdateFromDb()
                            me.iop.fixparlistrender.cook(force=True)
                            self.SetInitCue(1)                            
                            return 

                    
        

        if r[0]:

            ui.status="Ключ добавлен id: {}".format(r[1])
        else: 
            ui.status="При добавлении ключа что-то пошло не так"

        self.UpdateFromDb()
        me.iop.fixparlistrender.cook(force=True)
        self.SetInitCue(1)
    def CueDelete(self, row):
        row = int(row) - 1
        myCue=self.LocalCueData[row]
        answer=ui.messageBox('Вопросик', 'Уверены что хотите грохнуть ключ {}({},id:{}) и все его параметры?'.format(myCue.name, "%g"%myCue.order, myCue.id), buttons=['Да', 'Нет'])
        if answer==0:
            print ("Yes")
            r=self.executeUpdateQuery("DELETE FROM cue_float_data WHERE id_cue=%s", [myCue.id])
            r1=self.executeUpdateQuery("DELETE FROM cue WHERE id=%s", [myCue.id])
            if r[0] and r1[0]:
                ui.status="Ключ {} удалён".format(myCue.name)
            else: 
                ui.status="При удалении ключа что-то пошло не так"
        self.UpdateFromDb()
        me.iop.fixparlistrender.cook(force=True)
        self.SetInitCue(1)

        pass

    def Reloadsql(self):
        self.LocalCueData = []
        self.LocalCueDataByID = dict()
        self.LocalFixtureData = []
        self.LocalFixturesByID = dict()
        self.LocalFixturesByPath = dict()
        self.ActiveFields = []
        #self.DisconnectDb()
        #self.ConnectDb()
        self.UpdateFromDb()
        self.UpdateCueListRender()

    def UpdateFromDb(self):
        self.LoadCue()
        self.LoadFixtureData()
        self.LoadFixturePars()
        self.LoadCueFloatData()
        self.LoadCueFloatDataV2()
        self.ResortCuesByID()
        self.CreateActiveFields()
        
        pass

    def SetInitCue(self, val):
        # self.CueChangeByRow(val)
        self.UpdateCueListRender()
        self.RunCue(self.LocalCueDataByID[int(self.CurrentCueID)], momentary=1)

    def UpdateEveryFrame(self):
        self.q.UpdateEveryFrame()
        me.iop.activeparsrender.cook(force=True)
        if self.ExportMode == "ValueExport":
            self.ExportCopyAllPars()
        elif self.ExportMode == "ChopExport" and self.chopExportDisabled is not True:
            me.iop.floatsrender.cook(force=True)
        

        # проверяем, не изменился ли выбранный контейнер 
        self.autoSelectFixtureByCompName()

    def Clearselfixtures(self):
        self.lastActiveCompInUI.clear()
        self.autoSelectFixtureByCompName(isSomethingChanged=True, force=True)
        pass
    def autoSelectFixtureByCompName(self, isSomethingChanged=False, force=False):
        def findRowAndMakeList():
            myRowsToSelect=[]
            myRow=None
            for selFixId in self.lastActiveCompInUI.keys():
                if self.CueEditMode=="fixturesui":
                    myRow=self.ownerComp.I.uiFixtureModeFixlistWidget.op("out1")[str(selFixId),0]
                elif self.CueEditMode=="editmodeui":
                    myRow=self.ownerComp.I.uiEditModeFixlistWidget.op("out1")[str(selFixId),0]
                if myRow is not None:
                    myRowsToSelect.append(str(myRow.row))

            return myRowsToSelect
        
        if force or self.DeviceSelectMode!="Off":
            myAddedIndex=0
            for myFix in self.LocalFixtureData:
                if hasattr(op(myFix.global_object_location), "selected"):
                    
                    if getattr(op(myFix.global_object_location), "selected")==1:
                        myAddedIndex+=1
                        if myFix.id not in self.lastActiveCompInUI.keys():
                            # EVENT: выбран новый контейнер 
                            if self.DeviceSelectMode=="Switch1":
                                self.lastActiveCompInUI.clear()
                            myFix.is_selected=True
                            self.lastActiveCompInUI[myFix.id]=True
                            isSomethingChanged=True
                            
                            if self.DeviceSelectMode=="Switch1":
                                break

                    else:
                        if not self.DeviceSelectMode=="Switch1" and not self.DeviceSelectMode=="Add":
                            if myFix.id in self.lastActiveCompInUI.keys():
                                # EVENT: убран контейнер 
                                myFix.is_selected=False
                                isSomethingChanged=True
                                
                                
                                # print ("{}, {}, {}".format(len(self.lastActiveCompInUI), self.DeviceSelectMode, myAddedIndex))
                                self.lastActiveCompInUI.pop(myFix.id)

            if self.lastAddedFixtureIndex!=myAddedIndex and self.DeviceSelectMode=="Add" and myAddedIndex==0:
                self.DeviceSelectMode=3
            self.lastAddedFixtureIndex=myAddedIndex
            if isSomethingChanged:
                    # выключаем авто-режим вообще, если в режиме добавления выбрали не fixture-comp

                rowsToSelectList=findRowAndMakeList()
                # rowsToSelectList=
                # print (rowsToSelectList)
                rowsToSelectLine=" ".join(rowsToSelectList if self.DeviceSelectMode!="Switch1" else [rowsToSelectList[0]]) if len(rowsToSelectList)>0 else ""
                self.ownerComp.I.uiEditModeFixlistWidget.par.Selectedrows=rowsToSelectLine
                
    def SetActiveFixtureByPath(self, path):
        if len(ops(path)) > 0:
            if path in self.LocalFixturesByPath:
                myFix=self.LocalFixturesByPath[path]
                rowIndex=self.LocalFixtureData.index(myFix)
                
                self.FixtureRowsSelected=str(rowIndex)
    def UnselectAllActiveFixtures(self):
        self.FixtureRowsSelected=""
        


    def ExportCopyAllPars(self):
        for myField in self.ActiveFields:
            # TODO сделать чтобы отключённые ключи не работали 
            
#            if (myField.is_fading == 1 or myField.extra_export_frames >= 1) and myField.is_par_enabled:
            
            # ЕСЛИ ЕСТЬ ТАКОЙ ОБЪЕКТ 
            if hasattr(op(myField.fixture_object_location), "par"):
                # ЕСЛИ ЕСТЬ ТАКОЙ ПАРАМЕТР
                if hasattr(op(myField.fixture_object_location).par, myField.par_name):
                    thePar=getattr(op(myField.fixture_object_location).par, myField.par_name)
                    if len(myField.par_text_value)==0:
                        setattr(op(myField.fixture_object_location).par,
                                myField.par_name, myField.par_value)
                                
                    else:
                        setattr(op(myField.fixture_object_location).par,
                                myField.par_name, myField.par_text_value)

            if myField.is_fading == 0 and myField.extra_export_frames >= 1:
                    myField.extra_export_frames -= 1

        pass

    def UpdateCueListRender(self):
        me.iop.cuelist.cook(force=True)
        me.iop.fixlistrender.cook(force=True)
        me.iop.fixlistrender_orig_paths_for_edit.cook(force=True)
        me.iop.fixparlistrender.cook(force=True)
        me.iop.activeparsrender.cook(force=True)
        me.iop.activeparsrenderlive.cook(force=True)
        me.iop.storedat.cook(force=True)
        
    def FullReloadCuryCue(self):
        exec_string1='op("{}").allowCooking=False'.format(self.ownerComp.path)
        exec_string2='op("{}").allowCooking=False'.format(op(self.ownerComp.par.Ui).path)
        exec_string3='op("{}").allowCooking=True'.format(self.ownerComp.path)
        exec_string4='op("{}").allowCooking=True'.format(op(self.ownerComp.par.Ui).path)
        run(exec_string1, delayFrames=10)
        run(exec_string2, delayFrames=30)
        run(exec_string3, delayFrames=50)
        run(exec_string4, delayFrames=80)
    def BackupSqlDb(self, myfilename=None):
        
        extension = "sql"
        timestr = time.strftime("%Y%m%d-%H%M%S")
        path=project.folder
        if myfilename is not None:
            timestr=myfilename
        file_name = "{}/db/{}.{}".format(path, timestr, extension)
        dbPass=""
        if self.ownerComp.par.Dbpassword.eval()!='':
            dbPass=" -p{} ".format(self.ownerComp.par.Dbpassword.eval())
        exec_string="{}/db/mysqldump.exe --add-drop-table -h{} -u{} {} {} >{}".format(path,self.ownerComp.par.Dbhost, self.ownerComp.par.Dbuser, dbPass, self.ownerComp.par.Dbname, file_name)
        
        res=os.system(exec_string)
        print (exec_string)
        ui.status="Saved {}".format(file_name)
    def RestoreSqlDb(self, file):
        self.DisconnectDb()
        file_name = "{}/db/{}.{}".format(project.folder, file, "sql")
        dbPass=""
        if self.ownerComp.par.Dbpassword.eval()!='':
            dbPass=" -p{} ".format(self.ownerComp.par.Dbpassword.eval())        
        exec_string="{}/db/mysql.exe -h{} -u{} {} {} <{}".format(project.folder,self.ownerComp.par.Dbhost, self.ownerComp.par.Dbuser, dbPass, self.ownerComp.par.Dbname, file_name)
        run('import os')
        run('os.system("{}")'.format(exec_string), delayFrames=10)
        ui.status="Loaded {}".format(file_name)
        run('op("{}").FullReloadCuryCue()'.format(self.ownerComp.path), delayFrames=300)


    def CueChangeByRow(self, val):
        self.SetOwnerPar('Cuearrayindex', int(val))
        val -= 1
        cue = self.LocalCueData[int(val)]
        self.RunCue(cue)
        self.SetOwnerPar('Cueid', cue.id)
        self.SetOwnerPar('Cuename', cue.name)
        self.SetOwnerPar('Cueorder', cue.order)

    def FixInfoChangeByRow(self, val):
        self.SetOwnerPar('Cuearrayindex', int(val))
        val -= 1
        fix = self.LocalFixtureData[int(val)]
        self.SetOwnerPar('Fixtureidforinfo', fix.id)

    def SetNextExportMode(self):
        if int (self.ownerComp.par.Exportmode) < 2:
            self.ownerComp.par.Exportmode=int (self.ownerComp.par.Exportmode)+1
        else:
            self.ownerComp.par.Exportmode=0
        return
    def SetPrevExportMode(self):
        if int (self.ownerComp.par.Exportmode) > 0:
            self.ownerComp.par.Exportmode=int (self.ownerComp.par.Exportmode)-1
        else:
            self.ownerComp.par.Exportmode=2
        return

    def ExportmodeChanged(self, par, prev):
        if prev!=par:
            ui.status="Режим экспорта изменён на {}".format(par)
            if par == "ChopExport" and self.chopExportDisabled is not True:
                me.iop.floatsrender.export = True
            else:
                me.iop.floatsrender.export = False


    @property
    def CurrentCueID(self):
        __CurrentCueID = self.ownerComp.par.Cueid
        return self.ownerComp.par.Cueid

    @property
    def ExportMode(self):
        
        self.__ExportMode = self.ownerComp.par.Exportmode
        return self.ownerComp.par.Exportmode
    @ExportMode.setter
    def ExportMode(self, val):
        self.ownerComp.par.Exportmode=int(val)
        __ExportMode = int(val)
        return __ExportMode
    @property
    def DeviceSelectMode(self):
        __DeviceSelectMode = self.ownerComp.par.Autoselectdevicebycomp
        return __DeviceSelectMode
    @DeviceSelectMode.setter
    def DeviceSelectMode(self, val):
        self.ownerComp.par.Autoselectdevicebycomp=int(val)
        __DeviceSelectMode = int(val)
        return __DeviceSelectMode
    
    @property
    def FadesMode(self):
        __FadesMode = self.ownerComp.par.Fades
        return __FadesMode
    @FadesMode.setter
    def FadesMode(self, val):
        self.ownerComp.par.Fades.index=int(val)
        __FadesMode = int(val)
        return __FadesMode
    @property
    def ParsSelMode(self):
        __ParsSelMode = self.ownerComp.par.Parsselmode
        return __ParsSelMode
    @property
    def FixtureRowsSelected(self):
        __FixtureRowsSelected=self.ownerComp.I.uiEditModeFixlistWidget.par.Selectedrows
        return __FixtureRowsSelected
    @FixtureRowsSelected.setter
    def FixtureRowsSelected(self, val):
        myVal=""
        try:
            myVal=str(val)
        except:
            myVal=val
            ui.status = "Странняк при установке активного фиксчера!"
            print (ui.status)
        self.ownerComp.I.uiEditModeFixlistWidget.par.Selectedrows=myVal
        __FixtureRowsSelected=myVal
        return __FixtureRowsSelected
    @property
    def Curcuename(self):
        __Curcuename=self.ownerComp.par.Cuename
        return __Curcuename
    @property
    def Curcueid(self):
        __Curcueid=self.ownerComp.par.Cueid
        return __Curcueid
    @property
    def Curcueorder(self):
        __Curcueorder=self.ownerComp.par.Cueorder
        return __Curcueorder
        