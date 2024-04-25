import datetime 
from aiogram import types
from loader import db, bot
from aiogram.enums import ParseMode
from sqlite3 import Connection
from logging import getLogger

LOG = getLogger()

class DBCommands:
    pool: Connection = db
    ADD_NEW_USER = 'INSERT INTO workers (fullname) VALUES (:fullname)'
    ADD_DEP = 'UPDATE workers SET department=:department WHERE id=:id'
    DELETE_USER = 'DELETE FROM workers WHERE id=:id'
    CHECK_USER = 'SELECT * FROM workers w WHERE w.fullname LIKE :fullname'
    CHECK_SERT = 'SELECT * FROM sertificates s JOIN workers w ON w.id = s.worker_id WHERE w.id=:id'
    EDIT_USER = 'SELECT * FROM workers WHERE id=:id'
    ADD_APTEKA = 'UPDATE workers SET APTEKA="Да" where id=:id'
    ADD_HR = 'UPDATE workers SET ZKGU="Да" where id=:id'
    ADD_BGU_1 = 'UPDATE workers SET BGU_1="Да" where id=:id'
    ADD_BGU_2 = 'UPDATE workers SET BGU_2="Да" where id=:id'
    ADD_DIETA = 'UPDATE workers SET DIETA="Да" where id=:id'
    ADD_MIS = 'UPDATE workers SET MIS="Да" where id=:id'
    ADD_TIS = 'UPDATE workers SET TIS="Да" where id=:id'
    ADD_SED = 'UPDATE workers SET SED="Да" where id=:id'
    DELETE_APTEKA = 'UPDATE workers SET APTEKA="Нет" where id=:id'
    DELETE_HR = 'UPDATE workers SET ZKGU="Нет" where id=:id'
    DELETE_BGU_1 = 'UPDATE workers SET BGU_1="Нет" where id=:id'
    DELETE_BGU_2 = 'UPDATE workers SET BGU_2="Нет" where id=:id'
    DELETE_DIETA = 'UPDATE workers SET DIETA="Нет" where id=:id'
    DELETE_MIS = 'UPDATE workers SET MIS="Нет" where id=:id'
    DELETE_TIS = 'UPDATE workers SET TIS="Нет" where id=:id'
    DELETE_SED = 'UPDATE workers SET SED="Нет" where id=:id'
    EDIT_EMAIL = 'UPDATE workers SET EMAIL=:email where id=:id'
    ADD_NEW_SERT = 'INSERT INTO sertificates (worker_id, center_name, serial_number, date_start, date_finish)' \
                        'VALUES (:id, :center_name, :serial_number, :date_start, :date_finish)'
    CHECK_SERT_FIN = 'SELECT worker_id, center_name, serial_number, DATE_FINISH FROM sertificates '\
                        'WHERE date("now", "+30 days") > DATE_FINISH'
    FIND_WORKER = 'SELECT fullname FROM workers WHERE id = :id'
    ADD_PHONE = 'UPDATE workers SET telephone=:telephone WHERE id=:id'
    

    async def add_new_worker(self, fullname):
        args = {'fullname': fullname}
        command = self.ADD_NEW_USER
        worker_id = self.pool.execute(command, args)
        '''await bot.send_message(chat_id=-1002098726070, text=f"Пользователь {user.first_name} "\
                            f"{user.last_name} под ником @{user.username} добавил сотрудника {fullname} в матрицу",
                              parse_mode=ParseMode.HTML)'''
        self.pool.commit()

    async def plus_MIS(self, id):
        arg = {'id': id}
        command = self.ADD_MIS
        self.pool.execute(command, arg)
        self.pool.commit()

    async def plus_TIS(self, id):
        arg = {'id': id}
        command = self.ADD_TIS
        self.pool.execute(command, arg)
        self.pool.commit()

    async def plus_SED(self, id):
        arg = {'id': id}
        command = self.ADD_SED
        self.pool.execute(command, arg)
        self.pool.commit()

    async def plus_apteka(self, id):
        arg = {'id': id}
        command = self.ADD_APTEKA
        self.pool.execute(command, arg)
        self.pool.commit()

    async def plus_zkgu(self, id):
        arg = {'id': id}
        command = self.ADD_HR
        self.pool.execute(command, arg)
        self.pool.commit()

    async def plus_bgu1(self, id):
        arg = {'id': id}
        command = self.ADD_BGU_1
        self.pool.execute(command, arg)
        self.pool.commit()

    async def plus_bgu2(self, id):
        arg = {'id': id}
        command = self.ADD_BGU_2
        self.pool.execute(command, arg)
        self.pool.commit()

    async def plus_dieta(self, id):
        arg = {'id': id}
        command = self.ADD_DIETA
        self.pool.execute(command, arg)
        self.pool.commit()

    async def del_MIS(self, id):
        arg = {'id': id}
        command = self.DELETE_MIS
        self.pool.execute(command, arg)
        self.pool.commit()

    async def del_TIS(self, id):
        arg = {'id': id}
        command = self.DELETE_TIS
        self.pool.execute(command, arg)
        self.pool.commit()

    async def del_SED(self, id):
        arg = {'id': id}
        command = self.DELETE_SED
        self.pool.execute(command, arg)
        self.pool.commit()

    async def del_apteka(self, id):
        arg = {'id': id}
        command = self.DELETE_APTEKA
        self.pool.execute(command, arg)
        self.pool.commit()

    async def del_zkgu(self, id):
        arg = {'id': id}
        command = self.DELETE_HR
        self.pool.execute(command, arg)
        self.pool.commit()

    async def del_bgu1(self, id):
        arg = {'id': id}
        command = self.DELETE_BGU_1
        self.pool.execute(command, arg)
        self.pool.commit()

    async def del_bgu2(self, id):
        arg = {'id': id}
        command = self.DELETE_BGU_2
        self.pool.execute(command, arg)
        self.pool.commit()

    async def del_dieta(self, id):
        arg = {'id': id}
        command = self.DELETE_DIETA
        self.pool.execute(command, arg)
        self.pool.commit()

    async def check_worker(self, fullname, user):
        arg = {'fullname': f"%{fullname}%"}
        command = self.CHECK_USER
        result = self.pool.execute(command, arg)
        self.pool.commit()
        worker = result.fetchall()
        if len(worker) > 1 :
            await bot.send_message(chat_id=user, text='Пользователь с такими ФИО уже существует')
        else:
            return worker[0]
            

    async def view_worker(self, fullname, user):
        arg = {'fullname': f"%{fullname}%"}
        command = self.CHECK_USER
        result = self.pool.execute(command, arg)
        self.pool.commit()
        worker = result.fetchall()
        self.pool.commit()
        if len(worker) > 0:
            await bot.send_message(chat_id=user, text='По Вашему запросу найдены следующие пользователи:')
            for person in worker:
                access_dict = {
                    'Отделение': 'Нет',
                    '1С_Аптека': 'Нет',
                    '1С_Диетпитание': 'Нет',
                    '1С_ЗКГУ': 'Нет',
                    '1С_БГУ 1.0': 'Нет',
                    '1С_БГУ 2.0': 'Нет',
                    'СЭД': 'Нет',
                    'МИС': 'Нет',
                    'ТИС': 'Нет',
                    'email': 'Нет',
                    'телефон': 'Нет'
                    }
                person_list = []
                list_sert = []
                list_person = []
                arg_sert = {'id': int(person[0])}
                command_sert = self.CHECK_SERT
                result_sert = self.pool.execute(command_sert, arg_sert)
                worker_sert = result_sert.fetchall()
                sert_list = []
                for sert in worker_sert:
                    sert_list.append(f'УЦ - {sert[2]}')
                    sert_list.append(f'серийный номер - {sert[3]}')
                    sert_list.append(f'Начало действия - {sert[4]}')
                    sert_list.append(f"Окончание действия - {sert[5]}\n")
                access_dict['1С-Аптека'] = person[2]
                access_dict['1С_Диетпитание'] = person[6]
                access_dict['1С_ЗКГУ'] = person[3]
                access_dict['1С_БГУ 1.0'] = person[4]
                access_dict['1С_БГУ 2.0'] = person[5]
                access_dict['СЭД'] = person[9]
                access_dict['МИС'] = person[7]
                access_dict['ТИС'] = person[8]
                access_dict['email'] = person[10]
                access_dict['телефон'] = person[13]
                for key, value in access_dict.items():
                    if value != 'Нет' and value != '':
                        person_list.append(key)
                if 'email' in person_list:
                    num = person_list.index('email')
                    person_list[num] = f'email -  {access_dict["email"]}'
                if 'телефон' in person_list:
                    num = person_list.index('телефон')
                    person_list[num] = f'телефон: {access_dict["телефон"]}'
                list_sert = '\n'.join(sert_list)
                list_person = '\n'.join(person_list)
                await bot.send_message(chat_id=user, text=f'{person[1]}\n{person[12]}\nДоступы:\n' \
                                       f'{list_person}\n' \
                                       f'У сотрудника выпущены следующие сертификаты:\n' \
                                       f'\n{list_sert}'
                                        )

        else:
            await bot.send_message(chat_id=user, text='Такого пользователя нет в базе или ФИО написано неверно, попробуйте еще раз')

    async def view_worker_with_id(self, fullname, user):
        arg = {'fullname': f"%{fullname}%"}
        command = self.CHECK_USER
        result = self.pool.execute(command, arg)
        self.pool.commit()
        worker = result.fetchall()
        if len(worker) > 0:
            await bot.send_message(chat_id=user, text='По Вашему запросу найдены следующие пользователи:')
            for person in worker:
                list_sert = []
                list_person = []
                persons_id_list = []
                access_dict = {
                    'Отделение': 'Нет',
                    '1С_Аптека': 'Нет',
                    '1С_Диетпитание': 'Нет',
                    '1С_ЗКГУ': 'Нет',
                    '1С_БГУ 1.0': 'Нет',
                    '1С_БГУ 2.0': 'Нет',
                    'СЭД': 'Нет',
                    'МИС': 'Нет',
                    'ТИС': 'Нет',
                    'email': 'Нет',
                    'телефон': 'Нет'
                    }
                person_list = []
                arg_sert = {'id': int(person[0])}
                command_sert = self.CHECK_SERT
                result_sert = self.pool.execute(command_sert, arg_sert)
                worker_sert = result_sert.fetchall()
                sert_list = []
                for sert in worker_sert:
                    sert_list.append(f'УЦ - {sert[2]}')
                    sert_list.append(f'серийный номер - {sert[3]}')
                    sert_list.append(f'Начало действия - {sert[4]}')
                    sert_list.append(f"Окончание действия - {sert[5]}\n")
                access_dict['1С-Аптека'] = person[2]
                access_dict['1С_Диетпитание'] = person[3]
                access_dict['1С_ЗКГУ'] = person[4]
                access_dict['1С_БГУ 1.0'] = person[5]
                access_dict['1С_БГУ 2.0'] = person[6]
                access_dict['СЭД'] = person[7]
                access_dict['МИС'] = person[8]
                access_dict['ТИС'] = person[9]
                access_dict['email'] = person[10]
                access_dict['телефон'] = person[13]
                for key, value in access_dict.items():
                    if value != 'Нет' and value != '':
                        person_list.append(key)
                if 'email' in person_list:
                    num = person_list.index('email')
                    person_list[num] = f'email -  {access_dict["email"]}'
                if 'телефон' in person_list:
                    num = person_list.index('телефон')
                    person_list[num] = f'телефон: {access_dict["телефон"]}'
                list_sert = '\n'.join(sert_list)
                list_person = '\n'.join(person_list)
                await bot.send_message(chat_id=user, text=f'{person[1]}\n{person[12]}\nДоступы:\n' \
                                       f'{list_person}\n' \
                                       f'У сотрудника выпущены следующие сертификаты:\n' \
                                       f'\n{list_sert}'
                                        )
                persons_id_list.append(person[0])
            return persons_id_list
        else:
            return False

    async def del_worker(self, id):
        arg = {'id': id}
        command = self.DELETE_USER
        result = self.pool.execute(command, arg)
        self.pool.commit()
        return True
        
    async def view_worker_for_edition(self, id):
        arg = {'id': id}
        command = self.EDIT_USER
        result = self.pool.execute(command, arg)
        self.pool.commit()
        worker = result.fetchall()
        person_data = {'name': worker[0][1], '1С-Аптека': worker[0][2], '1С_ЗКГУ': worker[0][3], '1С_БГУ 1.0': worker[0][4],\
                       '1С_БГУ 2.0': worker[0][5], '1С_Диетпитание': worker[0][6], 'МИС': worker[0][7],'ТИС': worker[0][8],\
                        'СЭД': worker[0][9]}
        return person_data

    async def edit_email(self, id, email):
        args = {'id': id,
               'email': email
               }
        command = self.EDIT_EMAIL
        self.pool.execute(command, args)
        self.pool.commit()
    
    async def add_new_sert(self, worker_id, center_name, serial_number, date_start, date_finish):
        args = {
            'id': worker_id,
            'center_name': center_name,
            'serial_number': serial_number,
            'date_start': date_start,
            'date_finish': date_finish
        }
        command = self.ADD_NEW_SERT
        self.pool.execute(command, args)
        self.pool.commit()

    async def sert_ends(self, user):
        worker_command = self.CHECK_SERT_FIN
        sertificates = self.pool.execute(worker_command)
        self.pool.commit()
        await bot.send_message(chat_id=user, text=f'Сертификаты со скорым окончанием сроком действия:')
        for sert in sertificates.fetchall():
            arg = {'id': sert[0]}
            command = self.FIND_WORKER
            result = self.pool.execute(command, arg)
            worker = result.fetchall()
            self.pool.commit()
            await bot.send_message(chat_id=user, text=f'{worker[0][0]}\nЦентр сертификации - {sert[1]} \n' \
                                   f'Серийный номер - {sert[2]}\nДата окончания - {sert[3]}')
    
    async def add_department(self, worker_id, chat, dep):
        command = self.ADD_DEP
        args = {'id': worker_id,
                'department': dep
                }
        result = self.pool.execute(command, args)
        self.pool.commit()

    async def add_telephone(self, worker_id, phone):
        command = self.ADD_PHONE
        args = {'id': worker_id,
                'telephone': phone
                }
        result = self.pool.execute(command, args)
        self.pool.commit()
