import re
import copy
    
#------------------------------------------------------------------------------
#   resume parser 2022년11월 신규 포맷 start
#------------------------------------------------------------------------------
def resume_parser_202211(file_name):
    t0 = '^○\s*\개인정보\s*\수집•이용\s*\(필수사항\)'
    t1 = '^인적사항\s*\(필수\)'
    t2 = '^핵심역량\s*\(필수\)'
    t3 = '^학력사항\s*\(필수\)'
    t4 = '^경력사항 및 경력기술서\s*\(필수\)'
    t5 = '^희망근무조건\s*\(선택\)'
    t6 = '^채용우대자격\s*\(선택\)'
    t7 = '^어학\s*\(선택\)'
    t8 = '^자격증\s*\(선택\)'
    t9 = '^수상\s*\(선택\)'
    t10 = '^대외활동\s*\(선택\)'
    t11 = '^자기소개서\s*\(필수\)'
    t12 = '^지원자 :'

    main_tap = {
        'consent':  {'pattern':t0,         'val':'', 'cnt':0, 'tskip':False, 'tovar':''}, 
        'personalInfo':  {'pattern':t1,         'val':'', 'cnt':0, 'tskip':False, 'tovar':''}, 
        'coreCapability':  {'pattern':t2,         'val':'', 'cnt':0, 'tskip':False, 'tovar':''}, 
        'academicBackground':  {'pattern':t3,         'val':'', 'cnt':0, 'tskip':False, 'tovar':''}, 
        'career':  {'pattern':t4,         'val':'', 'cnt':0, 'tskip':False, 'tovar':''}, 
        'wishWorkplace':  {'pattern':t5,         'val':'', 'cnt':0, 'tskip':False, 'tovar':''}, 
        'preferential':  {'pattern':t6,         'val':'', 'cnt':0, 'tskip':False, 'tovar':''}, 
        'language':  {'pattern':t7,         'val':'', 'cnt':0, 'tskip':False, 'tovar':''}, 
        'license':  {'pattern':t8,         'val':'', 'cnt':0, 'tskip':False, 'tovar':''}, 
        'award':  {'pattern':t9,         'val':'', 'cnt':0, 'tskip':False, 'tovar':''}, 
        'activity':  {'pattern':t10,         'val':'', 'cnt':0, 'tskip':False, 'tovar':''}, 
        'introduce':  {'pattern':t11,         'val':'', 'cnt':0, 'tskip':False, 'tovar':''}, 
    }

    sub_datas = {
        'consent' : {
                        'useAgree' : { 'findStKey':'동의함(', 'findEdKey':') , 동의하지 않음', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                        'thirdpartyAgree' : {'findStKey':'동의함(', 'findEdKey':') , 동의하지 않음', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                        'ag_date' : {'findStKey':'', 'findEdKey':'', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                        'name' : {'findStKey':'본인 성명', 'findEdKey':'생년', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                        'birth' : {'findStKey':'생년', 'findEdKey':'이메일주소', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                        'email' : {'findStKey':'이메일주소', 'findEdKey':'휴대폰번호', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                        'phone' : {'findStKey':'휴대폰번호', 'findEdKey':'\n\n', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                        'skip' : {'findStKey':'', 'findEdKey':'', 'toval':'' , 'isRemoveEntered': False, 'isCheckBox':False} ,
                    },
        'personalInfo' : {
                            'name' :{ 'findStKey':'이름:', 'findEdKey':'생년월일:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'birth' :{ 'findStKey':'생년월일:', 'findEdKey':'휴대폰번호:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'phone' :{ 'findStKey':'휴대폰번호:', 'findEdKey':'이메일:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'email' :{ 'findStKey':'이메일:', 'findEdKey':'주소:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'address' :{ 'findStKey':'주소:', 'findEdKey':'최종연봉(', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'finalsalary' :{ 'findStKey':'최종연봉):', 'findEdKey':'', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                        },
        'coreCapability' : {
                            'main' :{ 'findStKey':'메인:', 'findEdKey':'상세:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'detail' :{ 'findStKey':'상세:', 'findEdKey':'기타:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'etc' :{ 'findStKey':'기타:', 'findEdKey':'', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                        },
                        
        'academicBackground' : {
                            'kindDetail' :{ 'findStKey':'[대학 이상]', 'findEdKey':'학교명:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': True},
                            'schoolName' :{ 'findStKey':'학교명:', 'findEdKey':'소재지:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'schoolLocation' :{ 'findStKey':'소재지:', 'findEdKey':'입학년월:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'entranceYear' :{ 'findStKey':'입학년월:', 'findEdKey':'졸업년월:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'graduationYear' :{ 'findStKey':'졸업년월:', 'findEdKey':'입학상태:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'entranceStatus' :{ 'findStKey':'입학상태:', 'findEdKey':'졸업상태:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': True},
                            'graduationStatus' :{ 'findStKey':'졸업상태:', 'findEdKey':'주전공:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': True},
                            'major' :{ 'findStKey':'주전공:', 'findEdKey':'학점:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'majorGrade' :{ 'findStKey':'학점:', 'findEdKey':'부전공:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'minor' :{ 'findStKey':'부전공:', 'findEdKey':'학점:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'minorGrade' :{ 'findStKey':'학점:', 'findEdKey':'[', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                        },
        'career' : {
                            'companyName' :{ 'findStKey':'회사명:', 'findEdKey':'입사년월:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'dateEntry' :{ 'findStKey':'입사년월:', 'findEdKey':'퇴사년월:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'dateResination' :{ 'findStKey':'퇴사년월:', 'findEdKey':'부서명:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'department' :{ 'findStKey':'부서명:', 'findEdKey':'직급:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'companyPosition' :{ 'findStKey':'직급:', 'findEdKey':'직책:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'companyDuty' :{ 'findStKey':'직책:', 'findEdKey':'최종연봉:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'subfinalSalary' :{ 'findStKey':'최종연봉:', 'findEdKey':'\n\n', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'detailsCompany' :{ 'findStKey':'경력기술:', 'findEdKey':'회사명:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                        },
        'wishWorkplace' : {
                            'employmentType':{ 'findStKey':'고용형태:', 'findEdKey':'입사가능시기:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': True},
                            'possibleDate':{ 'findStKey':'입사가능시기:', 'findEdKey':'희망근무지:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': True},
                            'wishWorkplace':{ 'findStKey':'희망근무지:', 'findEdKey':'희망직급:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': True},
                            'wishPosition':{ 'findStKey':'희망직급:', 'findEdKey':'희망연봉:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                            'wishSalary':{ 'findStKey':'희망연봉:', 'findEdKey':'', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox': False},
                        },
        'preferential' : {
                            'veterans':{ 'findStKey':'보훈대상 여부:', 'findEdKey':'장애여부:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox':True} ,
                            'disability':{ 'findStKey':'장애여부:', 'findEdKey':'병역:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox':True},
                            'military':{'key': ' ', 'findStKey':'병역:', 'findEdKey':'', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox':True},
                        },
        'language' : {
                            'language':{ 'findStKey':'', 'findEdKey':'', 'toval':'' , 'isRemoveEntered': False, 'isCheckBox':False} ,
                        },   
        'introduce' : {
            'introduce':{ 'findStKey':'', 'findEdKey':'상기 기재 사항은 허위 사실이 없음을 확인합니다', 'toval':'' , 'isRemoveEntered': False, 'isCheckBox':False} ,
        },                   
        'license' : {
                'license':{ 'findStKey':'', 'findEdKey':'', 'toval':'' , 'isRemoveEntered': False, 'isCheckBox':False} ,
        },  
        'award' : {
            'award':{ 'findStKey':'', 'findEdKey':'', 'toval':'' , 'isRemoveEntered': False, 'isCheckBox':False} ,
        },  
        'activity' : {
            'activity':{ 'findStKey':'', 'findEdKey':'', 'toval':'' , 'isRemoveEntered': False, 'isCheckBox':False} ,
        },  
                        
    }

    sub_datas_etc = {
        'academicBackground' : {
                            'schoolName':{'key': '', 'findStKey':'학교명:', 'findEdKey':'소재지:', 'toval':'' , 'isRemoveEntered': True,  'isCheckBox':False},
                            'schoolLocation':{'key': '', 'findStKey':'소재지:', 'findEdKey':'졸업년월:', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox':False},
                            'graduaionYear':{'key': '', 'findStKey':'졸업년월:', 'findEdKey':'[대학 이상]', 'toval':'' , 'isRemoveEntered': True, 'isCheckBox':False},
                        },
    }
    
    ts = '('+t1+'|'+t2+'|'+t3+'|'+t4+'|'+t5+'|'+t6+'|'+t7+'|'+t8+'|'+t9+'|'+t10+'|'+t11+'|'+t12+')'


    fi   = open(file_name,        'r', encoding = 'utf-8')

    

    # 각 섹션의 모든 데이터를 하나의 문장으로 만들기
    curr_mode = ''
    ag_date = ''
    while(True):

            line = fi.readline()
            
            if not line:
                break
            
            #--- /f 제거 ---    
            line = re.sub(r"\x0c", "", line)

            line1  = line.rstrip()

           

            for key, value in main_tap.items():
                
                m = re.search(value['pattern'], line1)
                if (m):
                    curr_mode = key
                    sub_flag = True
                    break
            
            if curr_mode != '' and not re.search(ts, line1):
                main_tap[curr_mode]['val'] += line


    # 데이타 취득하기
    for key, value in main_tap.items():
        
        _data = value['val']
        
        # 코드 위치 변경하면안됨
        idx = 0

        # 예외 처리부분 --- 시작
        # 고등학교 이력 예외 처리가 필요 (pattern 이 다름)                
        if key == 'academicBackground':
            for etckey, etcItems in sub_datas_etc[key].items():
                findStKey = etcItems['findStKey']
                findEdkey = etcItems['findEdKey']
                stLen = _data.find(findStKey,idx)+len(findStKey)
                edLen = _data.find(findEdkey,stLen)
                sub_datas_etc[key][etckey]['toval'] += returnValue(_data[stLen:edLen].lstrip(),etcItems)

        if key =='career':
            _data = re.sub(r'\[이하 선택사항\]','', _data)
            _data = re.sub(r'\==','', _data)

        if key == 'consent':
            match = re.search('(?P<year>\\d{4})\\s?년\\s*(?P<month>\\d{1,2})\\s*월\\s*(?P<day>\\d{1,2})\\s*일', _data)
            if (match is not None):
                ag_date = '%4d%02d%02d' % (int(match.groupdict()["year"]), int(match.groupdict()["month"]), int(match.groupdict()["day"]))
            
        # 예외 처리부분 --- 종료

        
        totalLen = len(_data)

        breakCnt = 0

        while(True):

            lastKey = 0

            breakCnt += 1

            # 데이터 형식변경에따른 무한루프 방지 
            if(breakCnt == 300):
                break

            if len(sub_datas[key]) == 0:
                break

            for subKey, items in sub_datas[key].items():
                
                findStKey = items['findStKey'] # 찾을 시작단어
                findEdkey = items['findEdKey'] # 찾을 끝단어

                stLen = _data.find(findStKey,idx)+len(findStKey)

                edLen = 0
                if findEdkey == '':
                    edLen = len(_data)
                else:
                    edLen = _data.find(findEdkey,stLen)

                if edLen == -1:
                    edLen = len(_data)

                idx = stLen
                lastKey = edLen + len(findEdkey)
                if subKey != 'skip':
                    if sub_datas[key][subKey]['toval'] != '':
                        sub_datas[key][subKey]['toval'] += '#@#'
                            
                    sub_datas[key][subKey]['toval'] += returnValue(_data[stLen:edLen].lstrip(),items) + ' '
                
            if (totalLen - lastKey) <= 0 or _data.find('상기 기재 사항은 허위 사실이 없음을 확인합니다') != -1:
                break
                    

    tmpAcademic = {
            'kindDetail' :'',
            'schoolName' :'',
            'schoolLocation' :'',
            'entranceYear' :'',
            'graduationYear' :'',
            'graduationStatus' :'',
            'major' :'',
            'majorGrade' :'',
            'minor' :'',
            'minorGrade' :'',
            }

    tmpCarrer =   {
                        'companyName' :'',
                        'dateEntry' :'',
                        'dateResination' : '',
                        'department' :'',
                        'companyPosition' :'',
                        'companyDuty' :'',
                        'subfinalSalary' :'',
                        'detailsCompany' :'',
                    }
    
    academicList = []
    careerList = []

    for key, value in main_tap.items():
        for subKey, items in sub_datas[key].items():
            #print(subKey+"::"+sub_datas[key][subKey]['toval'])
            
            if key == 'academicBackground':
                _datas = sub_datas[key][subKey]['toval'].split('#@#')
                for idx, val in enumerate(_datas):
                    # 복수건 처리를 위해서 배열을 추가한다
                    if subKey == 'kindDetail':
                        academicList.append(copy.deepcopy(tmpAcademic))
                    
                    academicList[idx][subKey] = val.rstrip()

            elif key =='career':
                _datas = sub_datas[key][subKey]['toval'].split('#@#')
                for idx, val in enumerate(_datas):
                    # 복수건 처리를 위해서 배열을 추가한다
                    if subKey == 'companyName':
                        careerList.append(copy.deepcopy(tmpCarrer))
                    
                    careerList[idx][subKey] = val.rstrip()
            else:
                sub_datas[key][subKey] = sub_datas[key][subKey]['toval'].rstrip()
            
                
    sub_datas['academicHighSchoolBackground'] = sub_datas_etc['academicBackground']
    sub_datas['academicBackground'] = academicList
    sub_datas['career'] = careerList
    sub_datas['consent']['ag_date'] = ag_date
    fi.close()

    return sub_datas

# 서브 펑션
def findChecked(data):
    rtnData = []
    for item in data:
        if(item.startswith('☒')):
            rtnData.append(item[1:])
    
    return rtnData

def removeEntered(data):
    return re.sub(r'\n','',data)
    
def returnValue(data, format):

    if(data.startswith('○○') or data.find('○○○') != -1):
        data = ''

    if data.rstrip() == '☒':
        data = 'true'

    if data.rstrip() == '☐':
        data = 'false'
    
    if format['isRemoveEntered']:
        data = removeEntered(data)

    # 필요 없는 내용 지우기
    data = re.sub(r'(☐해외|\(표시하지 않으면 내규에 따름\)|☐내규에따름)','',data)
        

    if format['isCheckBox']:
        return findChecked(data)
    else:
        return data


def findChecked(data):
    rtnData = ''
    for item in data.split():
        if(item.startswith('☒')):
            if rtnData != '':
                rtnData += '##' 

            rtnData += item[1:]
    
    return rtnData
#------------------------------------------------------------------------------
#   resume parser 2022년11월 신규 포맷 END
#------------------------------------------------------------------------------


#print(resume_parser_202211("RPA용 양식_확정.txt"))
#print(resume_parser_202211("동의서양식-R9용.txt"))
#print(resume_parser_202211("02_힌트텍스트 놔두고 기재.txt"))
#print(resume_parser_202211("03_학력 및 경력 복수기재.txt"))
print(resume_parser_202211("12_학력,경력 복수입력.txt"))


#print()


