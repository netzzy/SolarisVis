class FixtureUtils:
    def DeleteFixtureByID(self, id_fixture, info):
        ui.status=info['rowData']['id_fix']
        res=ui.messageBox('Вопросик', 'Уверены что хотите грохнуть девайс {}'.format(info['rowData']['Путь']), buttons=['Да', 'Нет'])
        if res==0 and int(id_fixture) > 0:
            self.executeUpdateQuery(
                "DELETE FROM fixture_float_data WHERE id_fixture=%s", [id_fixture])
            self.executeUpdateQuery(
                "DELETE FROM cue_float_data WHERE id_fixture=%s", [id_fixture])
            self.executeUpdateQuery(
                "DELETE FROM fixture WHERE id=%s", [id_fixture])
            self.UpdateFromDb()
            me.iop.fixparlistrender.cook(force=True)
            self.SetInitCue(1)
            ui.status="Fixture: удалён {} + его поля и ключи".format(info['rowData']['Путь'])

    def DeleteFixtureParByID(self, id_fix_par, id_fixture, par_name, info):
#        print ("Ёбт")
#       return 
        ui.status=info['rowData']['id']
        myPARinfo=info['rowData']['Параметр']
        res=ui.messageBox('Вопросик', 'Уверены что хотите грохнуть параметр {} из девайса и ключей?'.format(info['rowData']['Параметр']), buttons=['Да', 'Нет'])
        if res==0:
            print("{}, {}, {}".format(id_fixture, id_fix_par, par_name))
            self.executeUpdateQuery("DELETE FROM fixture_float_data WHERE id=%s", [id_fix_par])
            self.executeUpdateQuery("DELETE FROM cue_float_data WHERE id_fixture=%s and par_name=%s", [
                                    id_fixture, str(par_name)])
            # self.executeUpdateQuery(
            #     "DELETE FROM fixture_float_data WHERE id=%s", [id_fix_par])
            self.UpdateFromDb()
            me.iop.fixparlistrender.cook(force=True)
            self.SetInitCue(1)
            ui.status="Fixture: пар. {} его и ключи удалёны".format(myPARinfo)

    def DeleteCueParByID(self, id_fix_par, id_fixture, par_name, info):
        #res=ui.messageBox('Вопросик', 'Уверены что хотите грохнуть параметр {} из девайса и ключей?'.format(info['rowData']['Пар.']), buttons=['Да', 'Нет'])
        if int(info['rowData']['id'])==-1:
            ui.status="Поля {} нет в этом ключе, он задаётся где-то раньше".format(info['rowData']['Пар.'])
            return 
        print("{}, {}, {}".format(id_fixture, id_fix_par, par_name))
        self.executeUpdateQuery("DELETE FROM cue_float_data WHERE id_fixture=%s and par_name=%s and id_cue=%s", [
                                id_fixture, str(par_name), int(self.Curcueid)])
        # self.executeUpdateQuery(
        #     "DELETE FROM fixture_float_data WHERE id=%s", [id_fix_par])
        self.UpdateFromDb()
        me.iop.fixparlistrender.cook(force=True)
        self.SetInitCue(1)
        ui.status="Cues: поле {} удалёно из ключа".format(info['rowData']['Пар.'])
