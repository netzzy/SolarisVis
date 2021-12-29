from dataclasses import dataclass
from re import I
from typing import Any
import time
from queue import Queue
from random import randint

class InTableEditBase:
    def __init__(self, owner, info):
        self.qclass=owner
        self.info=info
        self.listPathToTable=[
            ('cue_float_data', ['CuryCueUI', 'CUES', 'CueParsList']),
            ('cue_float_data', ['CuryCueUI', 'EDITMODE', 'CueParsList']),
            ('cue', ['SHOWMODE_CUES', 'CueList']),
            ('cue', ['CUES', 'CueList']),
            ('cue', ['EDITMODE', 'CueList']),
            ('fixture', ['FIXTURES', 'FixList']),
            ('fixture_float_data', ['FIXTURES', 'FixParsList'])
        ]
        self._colHeadersToFields=dict()
        self.fqd=dict([
            ('col_header', ""),
            ('col_sql_name', ""),
            ('table_name', ""),
            ('prevValue', 0),
            ('newValue', 0),
            ('rec_id', 0),
            ('cue_id', 0)
        ])
    def UpdateDb(self):
        self.customLocalUpdate()
        self.qclass.UpdateFromDb()
        self.qclass.UpdateCueListRender()
        
        me.iop.fixparlistrender.cook(force=True)
        self.qclass.SetInitCue(1)

    def UpdateListCell(self):
        try:
            self.fqd['targetLister']=op(self.info['ownerComp'])
            self.customFillValuesFromCell()
        except:
            ui.status="Ошибка конвертации в UpdateListCell"

        if self.fqd['prevValue']==self.fqd['newValue']:
            ui.status="Запись не обновлена, так как значение идентичное предыдущему"
            return

        try:
            self.fqd['table_name']=self.getTableByListPath (self.info['ownerComp'].path)
            if self.customFillKeyData() is False:
                self.UpdateDb()
                return 
            self.fqd['col_header']=self.info['colName']
            # print (self.fqd['col_header'])
            self.fqd['col_sql_name']=self._colHeadersToFields[self.fqd['col_header']]

        except: 
            ui.status="Ошибка при обновлении поля - не найдено соответствие таблице или колонке"    

        (exec_status, exec_value)=self.customQuery()
        if exec_status:
            ui.status="Обновлена mysql запись в таблице {}, полю {} с ID {} присвоено значение {}".format(self.fqd['table_name'], self.fqd['col_sql_name'], self.fqd['rec_id'], self.fqd['newValue'])
            self.UpdateDb()
        else:
            ui.status=exec_value
    
    
    def getTableByListPath(self, path):
        path_list=path.split('/')
        
        for item in self.listPathToTable:
            (table, features)=item
            
            if all([(x in path_list) for x in features]):
                return table
class InTableCueListCellEdit (InTableEditBase):
    def __init__(self, owner, info):
        super().__init__(owner, info)
        self._colHeadersToFields=dict([
            ('Номер', 'order'),
            ('Название', 'name'),
            ('Комментарий', 'comment'),
            ('memo', 'memo'),
            ('linked', 'linked')
            
            ])        

    def customFillValuesFromCell(self):
        self.fqd['prevValue']=self.info['prevText']
        self.fqd['newValue']=self.info['text']
    def customFillKeyData(self):
        self.fqd['rec_id']=float(self.info['rowData']['id_cue'])
    def customQuery(self):
        query="UPDATE `{}` SET `{}` = %s WHERE {};".format(self.fqd['table_name'], self.fqd['col_sql_name'], "`id` = %s")
        (exec_status, exec_value)=self.qclass.executeUpdateQuery(query, [self.fqd['newValue'], self.fqd['rec_id']])
        return (exec_status, exec_value)
    def customLocalUpdate(self):
        setattr(self.qclass.LocalCueDataByID[self.fqd['rec_id']], self.fqd['col_sql_name'], self.fqd['newValue'])
class InTableCueParListCellEdit (InTableEditBase):
    def __init__(self, owner, info):
        super().__init__(owner, info)
        self._colHeadersToFields=_colHeadersToFields=dict([
                    ('Знач.', 'par_value'),
                    ('Fade', 'fade_in'),
                    ('Delay', 'delay_in')
                    ])    
        

    def customFillValuesFromCell(self):
        self.fqd['prevValue']=float(self.info['prevText'])
        self.fqd['newValue']=float(self.info['text'])
    def customFillKeyData(self):
        self.fqd["par_path"]=self.info['rowData']['Path']
        self.fqd['rec_id']=float(self.info['rowData']['id'])
        self.fqd['id_cue']=int(self.info['rowData']['id_cue'])
    def customQuery(self):
        query="UPDATE `{}` SET `{}` = %s WHERE {};".format(self.fqd['table_name'], self.fqd['col_sql_name'], "`id` = %s")
        # print ("Query: {}, args: {}", query, [self.fqd['newValue'], self.fqd['rec_id']])
        (exec_status, exec_value)=self.qclass.executeUpdateQuery(query, [self.fqd['newValue'], self.fqd['rec_id']])
        return (exec_status, exec_value)
    def customLocalUpdate(self):
        my_cue=self.qclass.LocalCueDataByID[self.fqd['id_cue']]
        setattr(my_cue.pars_float_by_path[self.fqd['par_path']], self.fqd['col_sql_name'], self.fqd['newValue'])
class InTableFixListCellEdit (InTableEditBase):
    def __init__(self, owner, info):
        super().__init__(owner, info)
        self._colHeadersToFields=dict([
            ('Сортировка', 'order'),
            ('Название', 'name'),
            ('Путь', 'global_object_location')
            ])        

    def customFillValuesFromCell(self):
        self.fqd['prevValue']=self.info['prevText']
        self.fqd['newValue']=self.info['text']
    def customFillKeyData(self):
        self.fqd['rec_id']=float(self.info['rowData']['id_fix'])
        self.fqd['pathkey']=self.info['rowData']['Путь']
    def customQuery(self):
        query="UPDATE `{}` SET `{}` = %s WHERE {};".format(self.fqd['table_name'], self.fqd['col_sql_name'], "`id` = %s")
        (exec_status, exec_value)=self.qclass.executeUpdateQuery(query, [self.fqd['newValue'], self.fqd['rec_id']])
        return (exec_status, exec_value)
    def customLocalUpdate(self):
        # setattr(self.qclass.LocalFixturesByPath[self.fqd['pathkey']], self.fqd['col_sql_name'], self.fqd['newValue'])
        self.qclass.UpdateFromDb()
        pass
class InTableFixListParEdit (InTableEditBase):
    def __init__(self, owner, info):
        super().__init__(owner, info)
        self._colHeadersToFields=dict([
            ('Default', 'default_value'),
            ('Параметр', 'par_name'),
            ('Вкл.', 'is_enabled')
            ])        

    def customFillValuesFromCell(self):
        self.fqd['prevValue']=self.info['prevText']
        self.fqd['newValue']=self.info['text']
    def customFillKeyData(self):
        self.fqd['rec_id']=float(self.info['rowData']['id'])
    def customQuery(self):
        query="UPDATE `{}` SET `{}` = %s WHERE {};".format(self.fqd['table_name'], self.fqd['col_sql_name'], "`id` = %s")
        (exec_status, exec_value)=self.qclass.executeUpdateQuery(query, [self.fqd['newValue'], self.fqd['rec_id']])
        return (exec_status, exec_value)
    def customLocalUpdate(self):
        pass
        #setattr(self.qclass.LocalFixturesByPath[self.fqd['pathkey']], self.fqd['col_sql_name'], self.fqd['newValue'])
class InTableActParEdit (InTableEditBase):
    def __init__(self, owner, info):
        super().__init__(owner, info)
        self._colHeadersToFields=dict([
            ('V db', 'par_value'),
            ('Fade', 'fade_in'),
            ('Delay', 'delay_in')
            ])        

    def customFillValuesFromCell(self):
        self.fqd['prevValue']=self.info['prevText']
        self.fqd['newValue']=self.info['text']
    def customFillKeyData(self):
        self.fqd['rec_id']=float(self.info['rowData']['id'])

        print ("huy {}".format(self.fqd['rec_id']))
        if int(self.fqd['rec_id'])==-1:
#            
            ui.status="Поле не существ. в ключе, задано раньше:пробуем добавить"
            (_status, _id)=self.qclass.Storeselected(updateDbAfter=False)
            if not _status:
                return False
            else:
                self.fqd['rec_id']=_id
            
    def customQuery(self):
        if self.fqd['col_sql_name']=="par_value":
            try:
                self.fqd['newValue']=float(self.fqd['newValue'])
            except: 
                try: 
                    self.fqd['newValue']=str(self.fqd['newValue'])
                except:
                    ui.status="Какой-то странный формат у {}".format(self.fqd['newValue'])
                    return False
                pass
        if self.fqd['col_sql_name']=="par_value":
            if isinstance(self.fqd['newValue'], str):
                self.fqd['col_sql_name']="par_text_value"
                print ("v: {}, t: {}".format(self.fqd['newValue'], self.fqd['col_sql_name']) )

        query="UPDATE `{}` SET `{}` = %s WHERE {};".format(self.fqd['table_name'], self.fqd['col_sql_name'], "`id` = %s")
        (exec_status, exec_value)=self.qclass.executeUpdateQuery(query, [self.fqd['newValue'], self.fqd['rec_id']])
        return (exec_status, exec_value)
    def customLocalUpdate(self):

        # setattr(self.qclass.LocalCueDataByID[self.fqd['rec_id']], self.fqd['col_sql_name'], self.fqd['newValue'])
        pass
        #setattr(self.qclass.LocalFixturesByPath[self.fqd['pathkey']], self.fqd['col_sql_name'], self.fqd['newValue'])
class InTableDataEdit:
    def __init__(self):
  
        pass
    def Callback_cue_list_mode_pars(self, mode, info):
        if info['callbackName']=="onEditEnd":
            updater=InTableCueParListCellEdit(self, info)
            updater.UpdateListCell()
        pass
    def Callback_edit_mode_pars(self, mode, info):
        if info['callbackName']=="onEditEnd":
            updater=InTableActParEdit(self, info)
            updater.UpdateListCell()
            
        pass
    
    def Callback_cue_list_mode_list(self, mode, info):
        if info['callbackName']=="onEditEnd":
            updater=InTableCueListCellEdit(self, info)
            updater.UpdateListCell()
        pass
    def Callback_fix_list_mode_list(self, mode, info):
        if info['callbackName']=="onEditEnd":
            updater=InTableFixListCellEdit(self, info)
            updater.UpdateListCell()
        pass
    def Callback_fix_par_mode_list(self, mode, info):
        if info['callbackName']=="onEditEnd":
            updater=InTableFixListParEdit(self, info)
            updater.UpdateListCell()
        pass
    def zapas(self):
        # {'prevText': '1', 
        # 'text': '2', 
        # 'rowData': OrderedDict([
        # ('id', '100'), 
        # ('id_cue', '2'), 
        # ('Девайс', 'Локальный свет'), 
        # ('Пар.', 'Level'), 
        # ('Знач.', '2'), 
        # ('Fade', '1.0'), 
        # ('Delay', '0.0'), 
        # ('Path', '/project1/LocalLights:Level'), 
        # ('Delete', 'x'), 
        # ('rowObject', ['100', '2', 'Локальный свет', 'Level', '1.0', '1.0', '0.0', '/project1/LocalLights:Level'])]), 
        # 'row': 6, 'col': 4, 
        # 'colName': 'Знач.', 
        # 'cellText': '2', 
        # 'ownerComp': type:listCOMP path:/project1/CuryCueUI/CUES/CueParsList/list/list/lister, 
        # 'callbackName': 'onEditEnd'}
        pass
