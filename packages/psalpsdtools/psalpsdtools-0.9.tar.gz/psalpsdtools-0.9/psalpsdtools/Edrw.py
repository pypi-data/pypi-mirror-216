from .PhRegPrv import PhRegPrv
from openpyxl import load_workbook
import os
#import xlrd
class Edrw:
    def __init__(self):
        pass
    def update_sources(self, regName, qtr, baseFolder, sdFile, commcode, yr):
        philippines = PhRegPrv()
        selected_provinces = philippines.get_provinces(regName)
        src = load_workbook(filename = baseFolder + "/" + sdFile, data_only=True)
        src_active = src["native B"]
        comm_arr = ["native","gamefowl","broiler","layer"]
        srv_arr = [" B"," C","_T"]

        if commcode == '08':
            if selected_provinces:
                for province in selected_provinces:
                    srcFile = str(commcode) + ' ' + str(province) + '_' + str(yr)
                    fileExt = '.xlsm'
                    fpath = str(baseFolder) + '/Sources/' + str(regName) + '/' + str(srcFile) + str(fileExt)
                    if os.path.isfile(fpath) == True:
                        for row in src_active.iter_rows(min_row=17, min_col=1, max_row=135, max_col=1):
                            for cell in row:
                                if cell.value == province:
                                    #print(f"{province} {cell.row}")
                                    rNumSrc = cell.row

                                    dst = load_workbook(filename=str(baseFolder) + '/Sources/' + str(regName) + '/' + str(srcFile) + str(fileExt))
                                    #dst = xlrd.open_workbook('Sources/' + str(regName) + '/' + str(srcFile) + str(fileExt))
                                    q1_dst_ws = dst[qtr]
                                    #q1_dst_ws = dst.sheet_by_name(qtr)

                                    if os.path.isfile(fpath) == True:
                                        for comm in comm_arr:
                                            for srv in srv_arr:
                                                if comm == "native":
                                                    if srv == " B":
                                                        rNumDst = 22
                                                    elif srv == " C":
                                                        rNumDst = 28
                                                    elif srv == "_T":
                                                        rNumDst = 34
                                                elif comm == "gamefowl":
                                                    if srv == " B":
                                                        rNumDst = 40
                                                    elif srv == " C":
                                                        rNumDst = 46
                                                    elif srv == "_T":
                                                        rNumDst = 52
                                                elif comm == "broiler":
                                                    if srv == " B":
                                                        rNumDst = 58
                                                    elif srv == " C":
                                                        rNumDst = 64
                                                    elif srv == "_T":
                                                        rNumDst = 70
                                                elif comm == "layer":
                                                    if srv == " B":
                                                        rNumDst = 76
                                                    elif srv == " C":
                                                        rNumDst = 82
                                                    elif srv == "_T":
                                                        rNumDst = 88

                                                sheetNameSrc = str(comm) + str(srv)
                                                qtr_src_ws = src[sheetNameSrc]
                                                print(f"PSA-LPSD (EDRW): Loading source -> {province} - {comm} - {srv}")

                                                if srv != "_T":
                                                    #print(f"Copying Source B{rNumSrc} to E{rNumDst}")
                                                    q1_dst_ws['E' + str(rNumDst)].value = qtr_src_ws['B' + str(rNumSrc)].value
                                                    q1_dst_ws['F' + str(rNumDst)].value = qtr_src_ws['C' + str(rNumSrc)].value
                                                    q1_dst_ws['H' + str(rNumDst)].value = qtr_src_ws['E' + str(rNumSrc)].value
                                                    q1_dst_ws['I' + str(rNumDst)].value = qtr_src_ws['F' + str(rNumSrc)].value
                                                    q1_dst_ws['J' + str(rNumDst)].value = qtr_src_ws['G' + str(rNumSrc)].value
                                                    q1_dst_ws['M' + str(rNumDst)].value = qtr_src_ws['J' + str(rNumSrc)].value
                                                    q1_dst_ws['N' + str(rNumDst)].value = qtr_src_ws['K' + str(rNumSrc)].value
                                                    q1_dst_ws['Q' + str(rNumDst)].value = qtr_src_ws['N' + str(rNumSrc)].value
                                                    q1_dst_ws['R' + str(rNumDst)].value = qtr_src_ws['U' + str(rNumSrc)].value
                                                    q1_dst_ws['S' + str(rNumDst)].value = qtr_src_ws['V' + str(rNumSrc)].value
                                                    q1_dst_ws['V' + str(rNumDst)].value = qtr_src_ws['Y' + str(rNumSrc)].value
                                                    q1_dst_ws['X' + str(rNumDst)].value = qtr_src_ws['AA' + str(rNumSrc)].value
                                                elif srv == "_T":
                                                    if comm == "native" or comm == "broiler" or comm == "layer":
                                                        q1_dst_ws['AA' + str(rNumDst)].value = qtr_src_ws['AD' + str(rNumSrc)].value
                                                    if comm == "broiler" or comm == "layer":
                                                        q1_dst_ws['AC' + str(rNumDst)].value = qtr_src_ws['AF' + str(rNumSrc)].value
                                                print(f"PSA-LPSD (EDRW): Copied to destination -> {province} - {comm} - {srv} at row {rNumSrc}")

                                        fpath = str(baseFolder) + '/Final/' + str(regName)
                                        if os.path.isdir(fpath) == False:
                                            os.mkdir(fpath)
                                        finalFile = str(baseFolder) + '/Final/' + str(regName) + '/' + str(commcode) + ' ' + str(province) + '_' + str(yr) + '.xls'
                                        print(f"PSA-LPSD (EDRW): Saving to file -> {finalFile}")
                                        dst.save(finalFile)
                                    else:
                                        print(f"File {srcFile}{fileExt} Not Found.")
                    else:
                        print(f"File {srcFile}{fileExt} Not Found.")
            else:
                print("Region not found or has no provinces.")
        else:
            print(f"Commodity code {commcode} not found.")
            