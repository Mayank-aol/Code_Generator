import teradatasql
import getpass
from pandas import read_excel
import os.path
from os import path
import datetime


# Function to generate the list of columns and datatype
def col_list():
    """This Function generates the list of columns and datatype"""

    print("\n", end="")
    no_of_col = int(input("Enter No of columns to be added in Header Tables: "))
    noc = 1
    list_of_columns = []
    while noc <= no_of_col:
        print("\n", end="")
        column_name = input("Enter Column Name to be added: ")
        data_type = input("Enter Data Type for the column: ")
        list_of_columns.append([column_name, data_type])
        noc += 1

    return list_of_columns


# Function to Alter Tables dedicated for Tables as per input file
def alter_table_func(list_of_cols, file_name):
    """This Function add columns returned by col_list function"""

    df = read_excel(file_name, sheet_name='Tables')
    list_of_tables = list(df['Table_Name'])

    with open('ALTER_TABLES.SQL', 'w+') as file_alt:
        no_of_col = len(list_of_cols)
        for table_name in list_of_tables:
            sql = "ALTER TABLE " + table_name + "\n"

            for i in range(0, no_of_col):
                if i < no_of_col - 1:
                    sql = sql + "ADD " + list_of_cols[i][0] + " " + list_of_cols[i][1] + " COMPRESS \n"

                elif i == no_of_col - 1:
                    sql = sql + "ADD " + list_of_cols[i][0] + " " + list_of_cols[i][1] + " COMPRESS;"

            # curs.execute(sql)
            print("/*****************" + "Alter Statement for " + table_name + "*****************/ \n\n", file=file_alt)
            print(sql, file=file_alt)
            print("/***********" + "*******" * 10 + "**********/ \n\n", file=file_alt)


# Function to Refresh Views definition as per input file
def replace_view_func(file_name):
    """This Function refresh views of Tables after addition of columns"""

    df = read_excel(file_name, sheet_name='Views')
    list_of_views = list(df['View_Name'])

    for views in list_of_views:
        sql = "SHOW VIEW " + views + ";"
        curs.execute(sql)
        with open('SV_' + views + ".sql", 'w+') as file_rep:
            for row in curs:
                print(row[0], file=file_rep, end="")

    with open('REPLACE_VIEWS.SQL', 'w') as file:
        for views in list_of_views:
            with open('SV_' + views + ".sql", 'r') as file_SV:
                cont = file_SV.readlines()

            print("/*****************" + "View Definition of " + views + "*****************/", file=file, end="")
            print("\n", file=file)
            for row in cont:
                print(row, file=file, end="")
                sql = sql + row
            print("\n", file=file)
            print("/***********" + "*******" * 10 + "**********/ \n", file=file)
            # curs.execute(sql)
            os.remove('SV_' + views + ".sql")


# Function to import definition of Macro as per input file into txt file
def replace_macro_to_file(file_name):
    """This Function imports the definition of macro and then fetch INSERT STATEMENT to a file"""

    df = read_excel(file_name, sheet_name='Macros')
    list_of_macros = list(df['Macro_Name'])
    for mc_name in list_of_macros:
        sql = "SHOW MACRO " + mc_name
        curs.execute(sql)
        source_file_name = 'RM_' + mc_name + '.sql'
        file = open(source_file_name, 'w+')
        for row in curs:
            print(row[0], file=file, end="")
        file.close()
        matched_lines = search_string_in_file(source_file_name, '**********/')

        if len(matched_lines) > 0:
            ele = matched_lines[0]
            line_number = int(ele[0])
            with open(source_file_name, 'r') as file:
                cont = file.readlines()
                no_of_lines = len(cont)

            target_file_name = 'MIS_' + mc_name + '.sql'
            with open(target_file_name, 'w+') as file_w:
                for i in range(line_number, no_of_lines):
                    print(cont[i], file=file_w, end="")


# Function to insert columns in Insert part of macro
def add_col_2_mc_insert(list_of_col_dtypes, file_name):
    """This function is used to add the columns to INSERT STATEMENT in a file"""

    df = read_excel(file_name, sheet_name='Macros')
    list_of_macros = list(df['Macro_Name'])
    for mc_name in list_of_macros:
        source_file_name = 'MIS_' + mc_name + '.sql'
        pos_of_col = search_string_in_file(source_file_name, ')')
        position = pos_of_col[0][0]
        separator = '\n\n     ,'
        col = ''
        list_of_col = []
        no_col = len(list_of_col_dtypes)

        for i in range(no_col):
            list_of_col.append(list_of_col_dtypes[i][0])

        for j in range(len(list_of_col)):
            col = separator.join(list_of_col)

        with open(source_file_name, 'r') as file:
            cont = file.readlines()

        cont.insert(position - 1, '     ,' + col + '\n\n')
        with open(source_file_name, 'w+') as file:
            cont = "".join(cont)
            file.write(cont)


# Function to insert column in Select part of Macro
def add_col_2_mc_outer_select(list_of_col_dtypes, file_name):
    """This function is used to add the columns to SELECT STATEMENT in a file which is source for INSERT"""

    df = read_excel(file_name, sheet_name='Macros')
    list_of_os_alias = list(df['OS_Alias'])
    list_of_macros = list(df['Macro_Name'])
    for i in range(len(list_of_macros)):
        source_file_name = 'MIS_' + list_of_macros[i] + '.sql'
        pos_of_col = search_string_in_file(source_file_name, 'FROM')
        position = pos_of_col[0][0]
        separator = '\n\n     ,'
        list_of_col = []
        no_col = len(list_of_col_dtypes)
        col = ''

        for j in range(no_col):
            list_of_col.append(list_of_col_dtypes[j][0])

        if type(list_of_os_alias[i]) == str:
            list_of_col = [list_of_os_alias[i] + '.' + col for col in list_of_col]

        for k in range(len(list_of_col)):
            col = separator.join(list_of_col)

        file = open(source_file_name, 'r')
        cont = file.readlines()
        file.close()

        cont.insert(position - 1, '     ,' + col + '\n\n')

        with open(source_file_name, 'w+') as file:
            cont1 = "".join(cont)
            file.write(cont1)


# Function to insert columns in inner select of Macro if Subquery present in Macro
def add_col_2_mc_inner_select(list_of_col_dtypes, file_name):
    """This function is used to add the columns to INNER SELECT STATEMENT in a file if macro have subquery
    in Source SELECT STATEMENT"""

    df = read_excel(file_name, sheet_name='Macros')
    list_of_macros = list(df['Macro_Name'])
    list_is_flag = list(df['IS_flag'])
    list_is_alias = list(df['IS_Alias'])

    for i in range(len(list_of_macros)):
        mc_name = list_of_macros[i]
        flag = list_is_flag[i]
        if flag == 'Y':
            source_file_name = 'MIS_' + mc_name + '.sql'
            pos_of_col = search_string_in_file(source_file_name, 'FROM ')
            position = pos_of_col[1][0]
            separator = '\n\n     ,'
            col = ''

            list_of_col = []
            for k in range(len(list_of_col_dtypes)):
                list_of_col.append(list_of_col_dtypes[k][0])

            if type(list_is_alias[i]) == str:
                list_of_col = [list_is_alias[i] + '.' + col for col in list_of_col]

            for j in range(len(list_of_col)):
                col = separator.join(list_of_col)

            file = open(source_file_name, 'r')
            cont = file.readlines()
            file.close()

            cont.insert(position - 1, '     ,' + col + '\n\n')
            file = open(source_file_name, 'w')
            cont = "".join(cont)
            file.write(cont)
            file.close()


# Function to insert columns in Group by statement of subquery in a Macro
def add_col_2_mc_subquery_grpby(list_of_col_dtypes, file_name):
    """This Function is used to add columns to group by statements in case of subquery"""

    print("GROUP BY Column addition started \n")
    df = read_excel(file_name, sheet_name='Macros')
    list_of_macros = list(df['Macro_Name'])
    list_of_grpby_flag = list(df['GRPBY_Flag'])
    list_of_grpby_keyword = list(df['GRPBY_Keyword'])
    for i in range(len(list_of_macros)):
        mc_name = list_of_macros[i]
        print("Working on Macro - {}".format(mc_name))
        grpby_kw = list_of_grpby_keyword[i]
        grpby_flag = list_of_grpby_flag[i]
        if grpby_flag == 'Y':
            source_file_name = 'MIS_' + mc_name + '.sql'
            pos_of_col = search_string_in_file(source_file_name, grpby_kw)
            position = pos_of_col[0][0]
            separator = '\n\n     ,'
            col = ''
            list_of_col = []

            for j in range(len(list_of_col_dtypes)):
                list_of_col.append(list_of_col_dtypes[j][0])

            for k in range(len(list_of_col)):
                col = separator.join(list_of_col)

            file = open(source_file_name, 'r')
            cont = file.readlines()
            file.close()

            cont.insert(position - 1, '     ,' + col + '\n\n')
            file = open(source_file_name, 'w')
            cont = "".join(cont)
            file.write(cont)
            file.close()
        print("Worked on Macro - {} completed. \n".format(mc_name))
    print("GROUP BY Column addition Finished SuccessFully")


# Function to add Comments in Macro Definition
def adding_comments_to_rm_statement(file_name, chng_typ_rqn, cmnt_reg_upd):
    """Function to add comment into the macro about details of addition"""

    df = read_excel(file_name, sheet_name='Macros')
    list_of_macros = list(df['Macro_Name'])
    for i in range(len(list_of_macros)):
        mc_name = list_of_macros[i]
        source_fn1 = 'RM_' + mc_name + '.sql'
        source_fn2 = 'MIS_' + mc_name + ".sql"
        matched_lines = search_string_in_file(source_fn1, '**********/')
        ele = matched_lines[0]
        line_no = int(ele[0])
        file_s1 = open(source_fn1, 'r')
        cont = file_s1.readlines()
        # no_of_lines = len(cont)
        file_s1.close()

        file_s2 = open(source_fn2, 'r')
        cont2 = file_s2.readlines()
        file_s2.close()

        date = str(datetime.datetime.now().date())

        cont.insert(line_no - 1,
                    '        ' + chng_typ_rqn + " - " + user_name + " - " + date + " - " + cmnt_reg_upd + '\n')
        comments = cont[:line_no + 1]
        target_fn = 'CRMS_' + mc_name + '.sql'

        file_t = open(target_fn, 'w+')
        for j in range(len(comments)):
            print(comments[j], file=file_t, end="")

        # print("\n", file=file_t)

        for k in range(len(cont2)):
            print(cont2[k], file=file_t, end="")


# Function to refresh Macro Definition.
def exe_refresh_macro(file_name):
    """This generates and returns a variable which will be executed later to refresh macro definition"""

    df = read_excel(file_name, sheet_name='Macros')
    list_of_macros = list(df['Macro_Name'])
    for mc_name in list_of_macros:
        source_fn = 'CRMS_' + mc_name + '.sql'
        file = open(source_fn, 'r')
        cont = file.readlines()
        no_of_ln = len(cont)
        sql = ""
        for i in range(no_of_ln):
            sql += cont[i]

        # curs.execute(sql)


# Function to delete all temporary_files:
def del_rename_temp_bkp_files(file_name):
    """This Function deletes all temp files and create backup of previous version and new version of macro in file"""

    df = read_excel(file_name, sheet_name='Macros')
    list_of_macros = list(df['Macro_Name'])

    for mc_name in list_of_macros:
        bkp_src_fn = 'RM_' + mc_name + '.sql'
        bkp_fn = 'BKP_VER_' + mc_name + '.sql'
        del_fn = 'MIS_' + mc_name + '.sql'
        curr_src_fn = 'CRMS_' + mc_name + '.sql'
        curr_fn = 'CURR_VER_' + mc_name + '.sql'

        if path.exists(bkp_fn):
            os.remove(bkp_fn)

        if path.exists(curr_fn):
            os.remove(curr_fn)

        os.rename(bkp_src_fn, bkp_fn)
        os.remove(del_fn)
        os.rename(curr_src_fn, curr_fn)


# Function to search a string in a file
def search_string_in_file(file_name, string_to_search):
    """Function is used to search any string in any file and returns its position with all occurrences and Line
    in which it is present"""

    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append([line_number, line.rstrip()])
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results


# Function to call all required functions for changes
def change_call_func(list_of_col_dtypes, file_name, chng_typ_rqn, cmnt_reg_upd):
    alter_table_func(list_of_col_dtypes, file_name)
    replace_view_func(file_name)
    replace_macro_to_file(file_name)
    add_col_2_mc_insert(list_of_col_dtypes, file_name)
    add_col_2_mc_outer_select(list_of_col_dtypes, file_name)
    add_col_2_mc_inner_select(list_of_col_dtypes, file_name)
    add_col_2_mc_subquery_grpby(list_of_col_dtypes, file_name)
    adding_comments_to_rm_statement(file_name, chng_typ_rqn, cmnt_reg_upd)
    exe_refresh_macro(file_name)
    del_rename_temp_bkp_files(file_name)


# Function for changes related to Orders and Products Team
def orders_ebia():
    print("\nPlease Press suitable option for Project Selection: \n")
    print("Press 1: For Orders_Header.\n"
          "Press 2: For Orders_Details. \n"
          "Press 3: For RTB. \n"
          "Press 4: For ISG. \n"
          "Press 5: For DTCP.\n")

    proj = int(input("Choose your input: "))

    if proj == 1:
        print("We are making changes in Order Header Project From Orders and Products Team. \n")
        print("Please Press suitable option for End Layer Selection: ")
        print("Press 1: For PKG.\n"
              "Press 2: For D3. \n")

        layer = int(input("Choose End Layer: "))

        if layer == 1:
            list_of_col_dtypes = col_list()
            chng_typ_rqn = input("Please enter Change type and change req no: \n"
                                 "(for Ex: <DTCP> - <CHG*****>)")
            cmnt_reg_upd = input("Please enter small description about changes \n"
                                 "(for Ex:Added TLA Attributes - 11 columns):")

            change_call_func(list_of_col_dtypes, 'SOHF_PKG.xlsx', chng_typ_rqn, cmnt_reg_upd)

        elif layer == 2:
            list_of_col_dtypes = col_list()
            chng_typ_rqn = input("Please enter Change type and change req no: \n"
                                 "(for Ex: <DTCP> - <CHG*****>)")
            cmnt_reg_upd = input("Please enter small description about changes \n"
                                 "(for Ex:Added TLA Attributes - 11 columns):")
            change_call_func(list_of_col_dtypes, 'SOHF_PKG.xlsx', chng_typ_rqn, cmnt_reg_upd)
            change_call_func(list_of_col_dtypes, 'SOHF_D3.xlsx', chng_typ_rqn, cmnt_reg_upd)

    elif proj == 2:
        print("We are making changes in Order Details Project From Orders and Products Team. \n")

    elif proj == 3:
        print("We are making changes in RTB Project From Orders and Products Team. \n")

    elif proj == 4:
        print("We are making changes in ISG Project From Orders and Products Team. \n")

    elif proj == 5:
        print("We are making changes in DTCP Project From Orders and Products Team. \n")

    else:
        print("-------Please Select a Valid Project-------")
        orders_ebia()


# Function for changes related to Finance Team
def finance():
    pass


# Function for changes related to Finance Team.
def doms():
    pass


# Function for changes related to Finance Team.
def devops():
    pass


# Function to close all cursors in order to ensure No resources of teradata is wasted.
def close_cursor_alter():
    """This is used to close the teradata connection and related cursors"""

    curs.close()
    conn.close()
    print("\n Cursor and connection for Teradata closed Successfully \n", end="")


def main():
    """This is function which is skeleton of Whole Program Script"""

    print("\nPlease Press suitable option for team Selection: ")
    print("Press 1: For Orders and Products.\n"
          "Press 2: For Finance Team. \n"
          "Press 3: For DOMS Team. \n"
          "Press 4: For DevOps Team. \n")

    team = int(input("Choose your input: "))

    if team == 1:
        orders_ebia()
    elif team == 2:
        finance()
    elif team == 3:
        doms()
    elif team == 4:
        devops()
    else:
        print("-------Please Select a Valid Team-------")
        main()


if __name__ == '__main__':

    try:
        host_name = input("Enter DSN name for Teradata Login: ")
        user_name = input("Enter Username for Teradata login: ")
        password = getpass.getpass("Enter Password for Teradata Login: ")
        conn = teradatasql.connect(host=host_name, user=user_name, password=password, logmech='LDAP')
        curs = conn.cursor()

    except Exception as e1:
        print(e1)
        try:
            host_name = input("Enter DSN name for Teradata Login: ")
            user_name = input("Enter Username for Teradata login: ")
            password = getpass.getpass("Enter Password for Teradata Login: ")
            conn = teradatasql.connect(host=host_name, user=user_name, password=password, logmech='LDAP')
            curs = conn.cursor()

        except Exception as e2:
            print(e2)
            exit()

    try:
        main()
        close_cursor_alter()

    except Exception as e:
        print(e)
        close_cursor_alter()
