from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import teradatasql
import os.path
from os import path
from pandas import read_excel
import datetime
import logging
import shutil
import zipfile

code_file_path = os.getcwd()

# Function to render Sign_In Page at front End.
def sign_in_page(request):
    global logger, log_file, log_file_path, date_str
    date = datetime.datetime.now()
    os.chdir(code_file_path)
    date_str = date.strftime('%Y%m%d_%H%M%S')
    log_file = 'CodeGenerator_LogFiles' + date_str + '.log'
    folder = './Files/LogFiles/'
    log_file_path = os.path.join(folder, log_file)
    logger = logging.getLogger(log_file_path)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file_path, mode='w')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info('----------Sign in Page----------')
    return render(request, "Sign_in.html")


def redirect_page(request):
    return render(request, "Code_Generator.html")


# Function to collect input from Sign_In Page and render Team and Project Page at Front End
def code_generator(request):
    """This Function Collects input data from Sign Page and log in to Teradata
                create cursor and Render Teams Page at Front End"""

    if request.method == 'POST':
        global user_name, curs, conn
        try:
            host_name = request.POST["env"]
            user_name = request.POST["username"]
            password = request.POST["password"]
            os.chdir('./Files')
            if path.exists(user_name):
                shutil.rmtree(user_name)
            os.mkdir(user_name)
            os.chdir(user_name)
            os.mkdir('LogFiles')
            os.mkdir('SrcFiles')
            os.mkdir('TgtFiles')
            os.chdir(code_file_path)
            logger.info('----------Collected Inputs From Sign In Page as: ----------')
            logger.info('----------HostName:- {} ----------'.format(host_name))
            logger.info('----------UserName:- {} ----------'.format(user_name))
            logger.info('----------Logging in to Teradata ----------')
            conn = teradatasql.connect(host=host_name, user=user_name, password=password, logmech='LDAP')
            curs = conn.cursor()
            logger.info('----------Successfully Logged in to Teradata host : {} ----------'.format(host_name))
            return render(request, "Code_Generator.html")

        except Exception as e:
            messages.error(request, 'Log In Failed - {}' .format(e))
            logger.debug('---------- Sign In to Teradata Failed ----------')
            logger.error('---------- {} ----------'.format(e))
            return redirect('/')


# Function redirects to particular operation as per selection in Front End
def operation_selector(request):
    operation = request.POST["operation"]
    if operation == 'Column_Addition':
        logger.info('----------Redirecting to Column Addition to Existing Macro----------')
        return render(request, 'Code_Gen.html')

    elif operation == 'Create_Macro':
        logger.info('----------Redirecting to Creating New Macro----------')
        return render(request, 'Macro_Creation.html')

    else:
        messages.error(request, '----------Please Choose a Valid Option----------')
        return render(request, "Code_Generator.html")


# Function Collects data about Macro and further process create a file with Macro Definition
def macro_details_page(request):
    src_db_nm = request.POST["src_db"]
    src_tbl_nm = request.POST["src_tbl"]
    tgt_db_nm = request.POST["tgt_db"]
    tgt_tbl_nm = request.POST["tgt_tbl"]
    macro_database = request.POST["macro_db"]
    macro_name = request.POST["macro_nm"]
    purpose_of_macro = request.POST["purpose"]
    called_by = request.POST["used_by"]
    wf_folder = request.POST["wf_folder"]
    wf_name = request.POST["wf_name"]
    sess_name = request.POST["sess_name"]
    project_name = request.POST["Project_Name"]
    logger.info('----------Request Submitted Successfully----------')

    sql_src = "SELECT ColumnName FROM DBC.Columns \n " \
              "WHERE TABLENAME = " + "'" + src_tbl_nm + "'" + "\n " \
              "AND DATABASENAME = " + "'" + src_db_nm + "'\n" \
              "ORDER BY COLUMNID" + ";"

    logger.info('----------Fetching Columns for Source Table: {} ----------'.format(src_db_nm + "." + src_tbl_nm))

    sql_tgt = "SELECT ColumnName FROM DBC.Columns \n " \
              "WHERE TABLENAME = " + "'" + tgt_tbl_nm + "'" + "\n" \
              "AND DATABASENAME = " + "'" + tgt_db_nm + "'\n" \
              "ORDER BY COLUMNID" + "; "

    curs.execute(sql_src)
    list_of_source_columns = []
    for cn_src in curs.fetchall():
        src_column_name = cn_src[0]
        column_name_src = src_column_name.strip()
        list_of_source_columns.append(column_name_src)

    logger.info('----------Fetching Columns for Target Table: {} ----------'.format(tgt_db_nm + "." + tgt_tbl_nm))
    curs.execute(sql_tgt)
    list_of_target_columns = []
    for cn_tgt in curs.fetchall():
        tgt_column_name = cn_tgt[0]
        column_name_tgt = tgt_column_name.strip()
        list_of_target_columns.append(column_name_tgt)

    logger.info('----------Number of Columns in Source Table: {}----------'.format(len(list_of_source_columns)))
    logger.info('----------Number of Columns in Target Table: {}----------'.format(len(list_of_target_columns)))

    if len(list_of_source_columns) > 0:
        logger.info('----------Source Table has been Validated and Present in TeraData----------')
        if len(list_of_target_columns) > 0:
            logger.info('----------Target Table has been Validated and Present in TeraData----------')
            if len(list_of_target_columns) == len(list_of_source_columns):
                separator = ",\n\n      "
                cont_tgt = separator.join(list_of_target_columns)
                cont_src = separator.join(list_of_source_columns)
                date_macro = datetime.datetime.now().date()
                os.chdir(code_file_path)
                os.chdir('./Files/' + user_name + '/TgtFiles/')
                fp = os.getcwd()
                file_name = os.path.join(fp, 'MACRO_DEF_' + macro_name + '.sql')
                logger.info('----------Creating Macro Definition into MACRO_DEF_{}.sql---------'.format(macro_name))
                with open(file_name, 'w+') as macro_file:
                    print("REPLACE MACRO {}.{} \n\nAS(\n".format(macro_database, macro_name), file=macro_file)
                    print("/" + "*****" * 30, file=macro_file)
                    print("MACRO: {}.{}".format(macro_database, macro_name), file=macro_file)
                    print("PURPOSE: {}".format(purpose_of_macro), file=macro_file)
                    print("INPUT PARAMS: NONE", file=macro_file)
                    print("CALLED BY: THIS MACRO IS BEING CALLED FROM {}".format(called_by), file=macro_file)
                    print("{}: WORKFLOW_NAME: {}: SESSION_NAME: {}".format(wf_folder, wf_name, sess_name),
                          file=macro_file)
                    print("REVISION HISTORY: ", file=macro_file)
                    print("<PROJECT_NAME>--<RELEASE_NO>--<DEVELOPER_NAME>-", file=macro_file, end="")
                    print("-<DEVELOPED_DATE-YYYYMMDD>-<SHORT_DESCRIPTION_OF_CHANGES>", file=macro_file)
                    print(project_name + "--" + user_name + "--" + str(date_macro) + "--INITIAL VERSION",
                          file=macro_file)
                    print("*****" * 30 + "/ \n\n    ", file=macro_file)
                    print("INSERT INTO {}.{} \n (".format(tgt_db_nm, tgt_tbl_nm), file=macro_file)
                    print("     " + cont_tgt, file=macro_file)
                    print("\n ) \n\nSELECT \n", file=macro_file)
                    print("     " + cont_src, file=macro_file)
                    print("\nFROM {}.{};".format(src_db_nm, src_tbl_nm), file=macro_file)
                    print("\n);", file=macro_file)
                logger.info('----------Macro Created Successfully ----------')
                zip_download_package()
                return render(request, "Request_Complete.html")

            else:
                logger.error('----------Column Mismatch Between Source and Target Tables---------')
                messages.error(request, 'Request Failed - Please Refer Log Files in attached Package')
                # logger.info('----------Closing Cursors for Teradata----------')
                # close_cursor_alter()
                zip_download_package()
                return render(request, "Request_Failed.html")

        else:
            logger.error(
                '----------Target Table: {} does not exists in TD---------'.format(tgt_db_nm + "." + tgt_tbl_nm))
            messages.error(request, 'Request Failed - Please Refer Log Files in attached Package')
            # logger.info('----------Closing Cursors for Teradata----------')
            # close_cursor_alter()
            zip_download_package()
            return render(request, "Request_Failed.html")

    else:
        logger.error('----------Source Table: {} does not exists in TD---------'.format(src_db_nm + "." + src_tbl_nm))
        messages.error(request, 'Request Failed - Please Refer Log Files in attached Package')
        # logger.info('----------Closing Cursors for Teradata----------')
        # close_cursor_alter()
        zip_download_package()
        return render(request, "Request_Failed.html")


def upload_src_file(request):
    if request.method == 'POST':
        global filename, team, project, file,file_path
        logger.info('----------Collected Inputs about Flow to be changed: ----------')
        team = request.POST["team"]
        project = request.POST["project"]
        layer = request.POST["layer"]
        logger.info('----------Team: {}'.format(team))
        logger.info('----------Project: {}'.format(project))
        logger.info('----------End Layer for Change Reflection: {}'.format(layer))
        os.chdir(code_file_path)
        os.chdir('./Files/' + user_name + '/SrcFiles/')
        file_path = os.getcwd()
        file = project + "_" + layer + ".xlsx"
        filename = os.path.join(file_path, file)
        logger.info('----------FilesName with Path: {}'.format(filename))
        os.chdir(code_file_path)
        return render(request, "Upload_Src_File.html", {'file': file})


# Function to Collect input from Teams and Project project and render Column Details Page at Front End
def num_cols_page(request):
    """This Function Collects input data about Team, Project and End Layer
                And Render Columns Details Page at Front End"""

    if request.method == 'POST':

        file_item = request.FILES['file']
        os.chdir(file_path)
        with open(file_item.name, 'wb+') as destination:
            for chunk in file_item.chunks():
                destination.write(chunk)
        os.chdir(code_file_path)
        logger.info('----------Uploading File: {} ----------' .format(file_item.name))
        if os.path.isfile(filename):
            logger.info('----------{}----------'.format(filename))
            logger.info('----------Files Uploaded Successfully----------')
            return render(request, 'Num_Cols.html')

        else:
            logger.error('----------Uploaded File is invalid, Please upload : {}---------'.format(file))
            messages.error(request, 'Request Failed - Please Refer Log Files in attached Package')
            zip_download_package()
            return render(request, "Request_Failed.html")


# Function to collect input from Columns details and Render Comments Page at Front End
def add_comments_page(request):
    """This Function Collects input data about Columns Details
                And Render Comments Page at Front End"""

    if request.method == 'POST':
        logger.info('----------Collected Inputs about Columns to be Added: ----------')
        num_cols = int(request.POST["Num_Col"])
        logger.info('----------Number of Columns: {} ----------'.format(num_cols))
        global list_of_columns
        list_of_columns = []
        for i in range(1, num_cols + 1):
            column_name = request.POST["name_col_" + str(i)]
            data_type = request.POST["dt_col_" + str(i)]
            logger.info('----------Column_Name: {} and Datatype: {} ----------'.format(column_name, data_type))
            list_of_columns.append([column_name, data_type])
        return render(request, "add_comments.html")


# Function to collect input from Comment details and run backend script
def get_comments(request):
    """This Function collects input data from Comments Page and Trigger Backend Script
                Also It Render Request Completion at End"""

    if request.method == 'POST':
        logger.info('----------Collected Inputs about Comments to be Added: ----------')
        comments = request.POST["chng_dtls"]
        comment_desc = request.POST["chng_desc"]
        logger.info('----------Change Details: {} ----------'.format(comments))
        logger.info('----------Change Description: {} ----------'.format(comment_desc))
        try:
            logger.info('----------Request Submitted Successfully----------')
            change_call_func(list_of_columns, filename, user_name, comments, comment_desc)
            logger.info('----------Request Completed Successfully ----------')

            zip_download_package()
            return render(request, "Request_Complete.html")

        except Exception as e1:
            logger.debug('----------Request Failed----------')
            messages.error(request, 'Request Failed - Please Refer Log Files in attached Package')
            logger.error(e1)
            zip_download_package()
            return render(request, "Request_Failed.html")


# Function to Alter Tables dedicated for Tables as per input file
def alter_table_func(list_of_cols, file_name):
    """This Function add columns returned by col_list function"""

    logger.info('----------Column Addition in Tables Started----------')
    logger.info('----------{}----------' .format(file_name))

    df = read_excel(file_name, sheet_name='Tables')
    list_of_tables = list(df['Table_Name'])
    os.chdir(file_path)
    os.chdir('../TgtFiles')
    fp = os.getcwd()
    if len(list_of_tables) > 0:
        file = 'ALTER_TABLES.SQL'
        logger.info('----------Alter Statement Being written in file: {} Placed at: {}'.format(file, fp))
        with open(os.path.join(fp, file), 'w+') as file_alt:
            no_of_col = len(list_of_cols)
            for table_name in list_of_tables:
                logger.info('----------Column being added to table: {}----------'.format(table_name))
                sql = "ALTER TABLE " + table_name + "\n"

                for i in range(0, no_of_col):
                    if i < no_of_col - 1:
                        sql = sql + "ADD " + list_of_cols[i][0] + " " + list_of_cols[i][1] + " COMPRESS, \n"

                    elif i == no_of_col - 1:
                        sql = sql + "ADD " + list_of_cols[i][0] + " " + list_of_cols[i][1] + " COMPRESS;"

                try:
                    logger.info('----------Query Execution Started----------')
                    # curs.execute(sql)
                    print("/*****************" + "Alter Statement for " + table_name + "*****************/ \n\n",
                          file=file_alt)
                    print(sql, file=file_alt)
                    print("/***********" + "*******" * 10 + "**********/ \n\n", file=file_alt)
                    logger.info('----------Query Execution Completed ----------')

                except Exception as e2:
                    logger.debug('----------Query Execution Failed----------')
                    logger.error('{}'.format(e2))
                    exit(1)
    else:
        logger.info('----------Table List is Empty, Hence Escaping to Views----------')


# Function to Refresh Views definition as per input file
def replace_view_func(file_name, list_of_col_dtypes):
    """This Function refresh views of Tables after addition of columns"""

    logger.info('----------View Refresh is Started----------')
    logger.info('----------Fetching View Names and flag details from Excel Sheet----------')
    df = read_excel(file_name, sheet_name='Views')
    list_of_views = list(df['View_Name'])
    logger.info('----------View List has been fetched----------')
    list_of_flag = list(df['Col_Add_Flag'])
    logger.info('----------Column Addition Flag List has been fetched----------')
    n = len(list_of_views)
    fp = os.getcwd()
    if len(list_of_views) > 0:
        for i in range(n):
            flag = list_of_flag[i]
            views = list_of_views[i]
            sql = "SHOW VIEW " + views + ";"
            logger.info('----------Fetching View Definition for : {} ---------'.format(views))
            curs.execute(sql)
            sv_file = 'SV_' + views + ".sql"
            file_nm = os.path.join(fp, sv_file)
            logger.info('----------View Definition stored in temp File : {} ----------'.format(file_nm))
            with open(file_nm, 'w+') as file_rep:
                for row in curs:
                    print(row[0], file=file_rep, end="")
            logger.info('----------View Fetching Completed--------')
            if flag == 'Y':
                logger.info('----------For View: {} - Columns Addition is required---------'.format(views))
                logger.info('----------Deciding Place for addition of Columns---------')
                pos_of_cols = search_string_in_file(file_nm, ')')
                position = pos_of_cols[0][0]
                separator = '\n\n     ,'
                col = ''
                list_of_col = []
                no_col = len(list_of_col_dtypes)

                for k in range(no_col):
                    list_of_col.append(list_of_col_dtypes[k][0])

                for j in range(len(list_of_col)):
                    col = separator.join(list_of_col)

                with open(file_nm, 'r') as file:
                    cont = file.readlines()

                logger.info('----------Adding Columns to Temp Files----------')
                cont.insert(position - 1, '     ,' + col + '\n\n')
                with open(file_nm, 'w+') as file:
                    cont = "".join(cont)
                    file.write(cont)

                pos_of_cols2 = search_string_in_file(file_nm, 'FROM')
                position2 = pos_of_cols2[0][0]
                with open(file_nm, 'r') as file:
                    cont1 = file.readlines()

                cont1.insert(position2 - 1, '     ,' + col + '\n\n')
                with open(file_nm, 'w+') as file:
                    cont1 = "".join(cont1)
                    file.write(cont1)

        logger.info('----------Adding all View Definition to Single File: REPLACE_VIEWS.SQL----------')
        with open('REPLACE_VIEWS.SQL', 'w') as file:
            for views in list_of_views:
                with open('SV_' + views + ".sql", 'r') as file_SV:
                    cont = file_SV.readlines()

                print("/*****************" + "View Definition of " + views + "*****************/", file=file, end="")
                print("\n", file=file)
                sql = ''
                for row in cont:
                    print(row, file=file, end="")
                    sql = sql + row
                print("\n", file=file)
                print("/***********" + "*******" * 10 + "**********/ \n", file=file)
                logger.info('----------Executing SQL for Refreshing View: {}----------'.format(views))
                # curs.execute(sql)
                logger.info('----------Executed SQL for Refreshing View: {}----------'.format(views))
                os.remove('SV_' + views + ".sql")
                logger.info('----------Removed Temp Files for View: {} ----------'.format(views))
        logger.info('----------View Refresh Completed----------')

    else:
        logger.info('----------View List is Empty, Hence Escaping to Macros----------')


# Function to import definition of Macro as per input file into txt file
def replace_macro_to_file(file_name):
    """This Function imports the definition of macro and then fetch INSERT STATEMENT to a file"""

    logger.info('----------Macro Refresh is Started----------')
    logger.info('----------Fetching Macro Names from Excel Sheet----------')
    df = read_excel(file_name, sheet_name='Macros')
    list_of_macros = list(df['Macro_Name'])
    logger.info('-----------{}---{}--------------'.format(len(list_of_macros),list_of_macros))
    for mc_name in list_of_macros:
        sql = "SHOW MACRO " + mc_name
        logger.info('----------Fetching Macro Definition for Macro :{} ----------'.format(mc_name))
        curs.execute(sql)
        fp = os.getcwd()
        source_file_name = 'RM_' + mc_name + '.sql'
        logger.info('----------Macro Definition Being stored in Temp file : {}----------'.format(source_file_name))
        file = open(os.path.join(fp, source_file_name), 'w+')
        for row in curs:
            print(row[0], file=file, end="")
        file.close()
        logger.info('----------Separating Insert Query to separate Temp Files ----------')
        matched_lines = search_string_in_file(os.path.join(fp, source_file_name), '***************/')

        if len(matched_lines) > 0:
            ele = matched_lines[0]
            line_number = int(ele[0])
            with open(os.path.join(fp, source_file_name), 'r') as file:
                cont = file.readlines()
                no_of_lines = len(cont)

            target_file_name = 'MIS_' + mc_name + '.sql'
            with open(os.path.join(fp, target_file_name), 'w+') as file_w:
                for i in range(line_number, no_of_lines):
                    print(cont[i], file=file_w, end="")
            logger.info('----------Written Insert Query to separate Temp Files : {}----------'.format(target_file_name))


# Function to insert columns in Insert part of macro
def add_col_2_mc_insert(list_of_col_dtypes, file_name):
    """This function is used to add the columns to INSERT STATEMENT in a file"""

    logger.info('----------Adding Columns to Insert of Macros ----------')
    df = read_excel(file_name, sheet_name='Macros')
    logger.info('----------Fetching List of Macros----------')
    list_of_macros = list(df['Macro_Name'])
    fp = os.getcwd()
    for mc_name in list_of_macros:
        logger.info('----------Column Addition to Insert in Macro : {} ----------'.format(mc_name))
        src_file = 'MIS_' + mc_name + '.sql'
        source_file_name = os.path.join(fp, src_file)
        pos_of_col = search_string_in_file(source_file_name, ')')
        if len(pos_of_col) > 0:
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

            logger.info('----------Column added to Temp File in Insert Query for Macro: {}----------'.format(mc_name))

        else:
            logger.error('Unable to Find `)` in Macro Please check If you have selected Correct Macro---------- ')
            logger.debug('----------List Out of Index----------')
            exit(1)


# Function to insert column in Select part of Macro
def add_col_2_mc_outer_select(list_of_col_dtypes, file_name):
    """This function is used to add the columns to SELECT STATEMENT in a file which is source for INSERT"""

    logger.info('----------Adding Columns to Source(First Select Statement) of Macros ----------')
    df = read_excel(file_name, sheet_name='Macros')
    logger.info('----------Fetching List of Macros and Alias to be used----------')
    list_of_os_alias = list(df['OS_Alias'])
    list_of_macros = list(df['Macro_Name'])
    fp = os.getcwd()
    for i in range(len(list_of_macros)):
        mc_name = list_of_macros[i]
        logger.info('----------Column Addition to Source(First Select Statement) in Macro: {}---------'.format(mc_name))
        src_file = 'MIS_' + mc_name + '.sql'
        source_file_name = os.path.join(fp, src_file)
        pos_of_col = search_string_in_file(source_file_name, 'FROM')
        if len(pos_of_col) > 0:
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
            logger.info('----------Column added to Temp File in Select Query for Macro: {}----------'.format(mc_name))
        else:
            logger.error('Unable to Find `FROM` in Macro Please check If you have selected Correct Macro---------- ')
            logger.debug('----------List Out of Index----------')
            exit(1)


# Function to insert columns in inner select of Macro if Subquery present in Macro
def add_col_2_mc_inner_select(list_of_col_dtypes, file_name):
    """This function is used to add the columns to INNER SELECT STATEMENT in a file if macro have subquery
    in Source SELECT STATEMENT"""

    logger.info('----------Adding Columns to SubQuery(If Any) in Macros ----------')
    df = read_excel(file_name, sheet_name='Macros')
    logger.info('----------Fetching List of Macros,Flag and Alias to be used----------')
    list_of_macros = list(df['Macro_Name'])
    list_is_flag = list(df['IS_flag'])
    list_is_alias = list(df['IS_Alias'])
    fp = os.getcwd()
    for i in range(len(list_of_macros)):
        mc_name = list_of_macros[i]
        flag = list_is_flag[i]
        if flag == 'Y':
            logger.info('----------Adding Columns to Inner Select in Macro : {} ----------'.format(mc_name))
            src_file = 'MIS_' + mc_name + '.sql'
            source_file_name = os.path.join(fp, src_file)
            pos_of_col = search_string_in_file(source_file_name, 'FROM')
            if len(pos_of_col) > 0:
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
                logger.info('----------Added Columns to Inner Select in Macro : {} ----------'.format(mc_name))
            else:
                logger.error('----------Unable to Find 2nd Occurrence of `FROM` in Macro ----------')
                logger.error('----------Please check If you have selected Correct Macro---------- ')
                logger.debug('----------List Out of Index----------')
                exit(1)
        else:
            logger.info('--------Inner Select Flag is N, So not adding Columns to Macro : {} --------'.format(mc_name))
            logger.info('--------Column Addition to Inner Select is not required in Macro : {}--------'.format(mc_name))


# Function to insert columns in Group by statement of subquery in a Macro
def add_col_2_mc_subquery_grpby(list_of_col_dtypes, file_name):
    """This Function is used to add columns to group by statements in case of subquery"""

    logger.info('----------Adding Columns to GROUP BY clause (If Any) in Macros ----------')
    df = read_excel(file_name, sheet_name='Macros')
    logger.info('----------Fetching List of Macros,Flag and GRPBY_KeyWord to be used----------')
    list_of_macros = list(df['Macro_Name'])
    list_of_grpby_flag = list(df['GRPBY_Flag'])
    list_of_grpby_keyword = list(df['GRPBY_Keyword'])
    fp = os.getcwd()
    for i in range(len(list_of_macros)):
        mc_name = list_of_macros[i]
        logger.info('----------Working on Macro - {}----------'.format(mc_name))
        grpby_kw = list_of_grpby_keyword[i]
        grpby_flag = list_of_grpby_flag[i]
        if grpby_flag == 'Y':
            logger.info('----------Adding Columns to Group by for Macro: {}----------'.format(mc_name))
            src_file = 'MIS_' + mc_name + '.sql'
            source_file_name = os.path.join(fp, src_file)
            pos_of_col = search_string_in_file(source_file_name, grpby_kw)
            if len(pos_of_col) > 0:
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
                logger.info('----------Columns Added to Group by for Macro: {}----------'.format(mc_name))

            else:
                logger.error('----------Unable to Find `{}` in Macro ----------'.format(grpby_kw))
                logger.error('----------Please check If you have given Correct KeyWord---------- ')
                logger.debug('----------List Out of Index----------')
                exit(1)
        else:
            logger.info('--------Group By Flag is N, So not adding Columns to Macro : {} --------'.format(mc_name))
            logger.info('--------Column Addition to Group by is not required in Macro : {}--------'.format(mc_name))

        logger.info('----------Worked on Macro - {} completed.----------'.format(mc_name))
    logger.info('----------GROUP BY Column addition Finished SuccessFully----------')


# Function to add Comments in Macro Definition
def adding_comments_to_rm_statement(file_name, username, chng_typ_rqn, cmnt_reg_upd):
    """Function to add comment into the macro about details of addition"""

    logger.info('----------Adding Columns to GROUP BY clause (If Any) in Macros ----------')
    df = read_excel(file_name, sheet_name='Macros')
    logger.info('----------Fetching list of Macros From Excel------------')
    list_of_macros = list(df['Macro_Name'])
    fp = os.getcwd()
    for i in range(len(list_of_macros)):
        mc_name = list_of_macros[i]
        logger.info('----------Adding Comments to Macro : {}----------'.format(mc_name))
        src_fn1 = 'RM_' + mc_name + '.sql'
        src_fn2 = 'MIS_' + mc_name + ".sql"
        source_fn1 = os.path.join(fp, src_fn1)
        source_fn2 = os.path.join(fp, src_fn2)
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

        date_comments = str(datetime.datetime.now().date())

        cont.insert(line_no - 1,
                    '        ' + chng_typ_rqn + " - " + username + " - " + date_comments + " - " + cmnt_reg_upd + '\n')
        comments = cont[:line_no + 1]

        logger.info('----------Combining Temp files at creating single Temp File for whole Macro ----------')
        tgt_fn = 'CRMS_' + mc_name + '.sql'
        target_fn = os.path.join(fp, tgt_fn)
        file_t = open(target_fn, 'w+')
        for j in range(len(comments)):
            print(comments[j], file=file_t, end="")

        # print("\n", file=file_t)

        for k in range(len(cont2)):
            print(cont2[k], file=file_t, end="")
        logger.info('----------Comments added to Macro Temp Files----------')


# Function to refresh Macro Definition.
def exe_refresh_macro(file_name):
    """This generates and returns a variable which will be executed later to refresh macro definition"""

    logger.info('----------Executing Replace Macro to push changes from temp file to TD------------')
    df = read_excel(file_name, sheet_name='Macros')
    list_of_macros = list(df['Macro_Name'])
    fp = os.getcwd()
    for mc_name in list_of_macros:
        logger.info('----------Executing Refresh Macro for: {}----------'.format(mc_name))
        src_fn = 'CRMS_' + mc_name + '.sql'
        source_fn = os.path.join(fp, src_fn)
        file = open(source_fn, 'r')
        cont = file.readlines()
        no_of_ln = len(cont)
        sql = ""
        for i in range(no_of_ln):
            sql += cont[i]
        try:
            # curs.execute(sql)
            logger.info('----------Executed Refresh Macro for: {} Successfully----------'.format(mc_name))

        except Exception as e6:
            logger.debug('----------Execution of Refresh Macro have failed ----------')
            logger.error('{}'.format(e6))
            exit(1)


# Function to delete all temporary_files:
def del_rename_temp_bkp_files(file_name):
    """This Function deletes all temp files and create backup of previous version and new version of macro in file"""

    logger.info('----------Creating Backup of Previous Version and Deleting Temp Files----------')
    df = read_excel(file_name, sheet_name='Macros')
    logger.info('----------Fetching list of Macros from Excel----------')
    list_of_macros = list(df['Macro_Name'])
    fp = os.getcwd()
    for mc_name in list_of_macros:
        bkp_src_fn = 'RM_' + mc_name + '.sql'
        bkp_fn = 'BKP_VER_' + mc_name + '.sql'
        del_fn = 'MIS_' + mc_name + '.sql'
        curr_src_fn = 'CRMS_' + mc_name + '.sql'
        curr_fn = 'CURR_VER_' + mc_name + '.sql'

        logger.info('----------Removing Previous Backup Files for Macro: {}----------'.format(mc_name))
        if path.exists(os.path.join(fp, bkp_fn)):
            os.remove(os.path.join(fp, bkp_fn))

        if path.exists(os.path.join(fp, curr_fn)):
            os.remove(os.path.join(fp, curr_fn))
        logger.info('----------Creating New Backup Files for Macro : {}----------'.format(mc_name))
        os.rename(os.path.join(fp, bkp_src_fn), os.path.join(fp, bkp_fn))
        os.remove(os.path.join(fp, del_fn))
        os.rename(os.path.join(fp, curr_src_fn), os.path.join(fp, curr_fn))

    logger.info('----------Created Backup of Previous Version and Deleted all Temp Files----------')


def zip_download_package():
    os.chdir(code_file_path)
    shutil.copyfile(log_file_path, './Files/' + user_name + '/LogFiles/' + log_file)
    os.chdir('./Files')
    zip_file_path = os.getcwd()
    rel_path = zip_file_path + '/' + user_name
    zip_file = user_name + '_' + date_str + '.zip'
    zipper = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(zip_file_path + '/' + user_name):
        for file in files:
            zipper.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(rel_path, '..'
                                                                                                              )))
    zipper.close()
    os.chdir(code_file_path)


def download_package(request):
    os.chdir(code_file_path)
    os.chdir('./Files')
    zip_file = user_name + '_' + date_str + '.zip'
    if os.path.isfile(zip_file):
        response = HttpResponse(open(zip_file, 'rb'), content_type='application/zip')
        os.chdir(code_file_path)
        return response


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
def change_call_func(list_of_col_dtypes, file_name, username, chng_typ_rqn, cmnt_reg_upd):
    alter_table_func(list_of_col_dtypes, file_name)
    replace_view_func(file_name, list_of_col_dtypes)
    df = read_excel(file_name, sheet_name='Macros')
    list_of_mc = list(df['Macro_Name'])
    if len(list_of_mc) > 0:
        replace_macro_to_file(file_name)
        add_col_2_mc_insert(list_of_col_dtypes, file_name)
        add_col_2_mc_outer_select(list_of_col_dtypes, file_name)
        add_col_2_mc_inner_select(list_of_col_dtypes, file_name)
        add_col_2_mc_subquery_grpby(list_of_col_dtypes, file_name)
        adding_comments_to_rm_statement(file_name, username, chng_typ_rqn, cmnt_reg_upd)
        exe_refresh_macro(file_name)
        del_rename_temp_bkp_files(file_name)

    else:
        logger.info('----------Macro List is Empty, Closing Request----------')


# Function to close all cursors in order to ensure No resources of teradata is wasted.
def close_cursor():
    """This is used to close the teradata connection and related cursors"""

    curs.close()
    conn.close()
    os.chdir(code_file_path)
    logger.info('----------Cursor and connection for Teradata closed Successfully----------')


def logout(request):
    close_cursor()
    # os.remove('./Files/LogFiles/' + log_file)
    return render(request, 'LogOut.html')
