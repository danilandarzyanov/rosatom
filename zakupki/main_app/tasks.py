from celery import shared_task, current_task
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile, os, ftplib, requests
from bs4 import BeautifulSoup
from django.apps import apps
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zakupki.settings')


class ZakupkiParser:
    # FTP data
    url = "ftp.zakupki.gov.ru"
    login223 = 'fz223free'
    login44 = 'free'
    password223 = 'fz223free'
    password44 = 'free'

    # tmp directory
    tmp = Path(Path.cwd(), "tmp")

    # db data
    db_hostname = 'localhost'
    db_port = 5432
    db_name = 'zakupki'
    db_username = 'django'
    db_password = 'password'

    # лимит записей установлен только в целях отладки парсера
    limit_record = 500

    # получить последний или все имена файлов
    @staticmethod
    def get_file_names(ftp, path_on_ftp, last=True):
        ftp.cwd(path_on_ftp)
        file_names = []
        fls = ftp.nlst()
        fls_gen = [x for x in fls if x[-3:] == 'zip']
        if last:
            file_names.append(fls_gen[-1])
        else:
            file_names = fls_gen
        return file_names

    # скачать архивы
    @staticmethod
    def download_files(ftp, path_on_ftp, files, path_to_download):
        ftp.cwd(path_on_ftp)
        for file in files:
            with open(Path(path_to_download, file), 'wb') as upload_file:
                ftp.retrbinary('RETR ' + file, upload_file.write)

    # распокавать архивы
    @staticmethod
    def unzip_files(files, unzip_to):
        unzip_files = []
        for file in files:
            with zipfile.ZipFile(Path(unzip_to, file)) as zf:
                zf.extractall(path=Path(unzip_to))
            os.remove(Path(unzip_to, file))
        for file in os.listdir(unzip_to):
            if file.endswith(".xml"):
                unzip_files.append(Path(unzip_to,file))
        return unzip_files

    # получить необходимые xml-файлы
    def get_xml_files(self,  path_to_files, last=True, fz=233):
        with ftplib.FTP(self.url) as server:
            server.connect(self.url)
            if fz == 233:
                server.login(self.login223, self.password223)
            elif fz == 44:
                server.login(self.login44, self.password44)

            files_name = self.get_file_names(server, path_to_files, last)
            self.download_files(server, path_to_files, files_name, self.tmp)
            files_name = self.unzip_files(files_name, self.tmp)
            return files_name

    def parse_and_save_to_db(self, class_name, xml_files):
        records = []
        i = 0;
        for xml_file in xml_files:
            br = False
            xml = ET.parse(xml_file)
            root = xml.getroot()
            # парсинг nsiOkato
            if class_name == 'nsiOkato':
                namespace = "http://zakupki.gov.ru/223fz/reference/1"
                parent_dom = "nsiOkatoData"
                data = nsiOkato()

                items = root.findall(f".//{{{namespace}}}{parent_dom}")
                for item in items:
                    i += 1
                    try:
                        data.code = item.find(f".//{{{namespace}}}code").text
                        data.name = item.find(f".//{{{namespace}}}name").text
                        data.parent = item.find(f".//{{{namespace}}}parent").text if item.find(f".//{{{namespace}}}parent") is not None else None
                        data.save()
                    except Exception as e:
                        pass
                    if i > self.limit_record:
                        br = True
                        break
            if br:
                break

            if class_name == 'nsiOkdp':
                namespace = "http://zakupki.gov.ru/223fz/reference/1"
                parent_dom = "nsiOkdpData"
                data = nsiOkpd()

                items = root.findall(f".//{{{namespace}}}{parent_dom}")
                for item in items:
                    i += 1
                    try:
                        data.code = item.find(f".//{{{namespace}}}code").text
                        data.name = item.find(f".//{{{namespace}}}name").text
                        data.parent = item.find(f".//{{{namespace}}}parent").text if item.find(
                            f".//{{{namespace}}}parent") is not None else None
                        data.save()
                    except Exception as e:
                        pass
                    if i > self.limit_record:
                        br = True
                        break
            if br:
                break

            if class_name == 'nsiOkpd2':
                namespace = "http://zakupki.gov.ru/223fz/reference/1"
                parent_dom = "nsiOkpd2Data"

                items = root.findall(f".//{{{namespace}}}{parent_dom}")
                for item in items:
                    i += 1
                    try:
                        code = item.find(f".//{{{namespace}}}code").text
                        name = item.find(f".//{{{namespace}}}name").text
                        parent = item.find(f".//{{{namespace}}}parentCode").text
                        nsiOkpd2.objects.get_or_create(
                            code=code,
                            name=name,
                            parent=parent,
                        )
                    except Exception as e:
                        pass
                    if i > self.limit_record:
                        br = True
                        break
            if br:
                break

            if class_name == 'nsiOkei':
                namespace = "http://zakupki.gov.ru/223fz/reference/1"
                parent_dom = "nsiOkeiData"

                items = root.findall(f".//{{{namespace}}}{parent_dom}")
                for item in items:
                    i += 1
                    try:
                        data = nsiOkei()
                        data.code = item.find(f".//{{{namespace}}}code").text
                        data.name = item.find(f".//{{{namespace}}}name").text
                        data.parent = item.find(f".//{{{namespace}}}parent").text if item.find(
                            f".//{{{namespace}}}parent") is not None else None

                        code = item.find(f".//{{{namespace}}}section").find(f".//{{{namespace}}}code").text
                        name = item.find(f".//{{{namespace}}}section").find(f".//{{{namespace}}}name").text
                        dataSection, create = nsiOkeiSection.objects.get_or_create(
                            code=code,
                            name=name,
                        )
                        data.section_id = dataSection.id
                        code = item.find(f".//{{{namespace}}}group").find(f".//{{{namespace}}}code").text
                        name = item.find(f".//{{{namespace}}}group").find(f".//{{{namespace}}}name").text
                        dataGroup, create = nsiOkeiGroup.objects.get_or_create(
                            code=code,
                            name=name,
                        )
                        data.group_id = dataGroup.id
                        data.save()
                    except Exception as e:
                        pass
                    if i > self.limit_record:
                        br = True
                        break
            if br:
                break

            if class_name == 'nsiOkogu':
                namespace = "http://zakupki.gov.ru/223fz/reference/1"
                parent_dom = "nsiOkoguData"
                items = root.findall(f".//{{{namespace}}}{parent_dom}")
                for item in items:
                    i += 1
                    try:
                        code = item.find(f".//{{{namespace}}}code").text
                        name = item.find(f".//{{{namespace}}}name").text
                        parent = item.find(f".//{{{namespace}}}parentCode").text if item.find(f".//{{{namespace}}}parentCode") is not None else None
                        nsiOkogu.objects.get_or_create(code=code, name=name, parent=parent)

                    except Exception as e:
                        print(e)
                        pass
                    if i > self.limit_record:
                        br = True
                        break
            if br:
                break

                # парсинг nsiOkfs
            if class_name == 'nsiOkfs':
                namespace = "http://zakupki.gov.ru/223fz/reference/1"
                parent_dom = "nsiOkfsData"
                data = nsiOkfs()

                items = root.findall(f".//{{{namespace}}}{parent_dom}")
                for item in items:
                    i += 1
                    try:
                        code = item.find(f".//{{{namespace}}}code").text
                        name = item.find(f".//{{{namespace}}}name").text
                        nsiOkfs.objects.get_or_create(
                            code=code,
                            name=name,
                        )
                    except Exception as e:
                        pass
                    if i > self.limit_record:
                        br = True
                        break
            if br:
                break

            if class_name == 'nsiOktmo':
                namespace = "http://zakupki.gov.ru/223fz/reference/1"
                parent_dom = "nsiOktmoData"

                items = root.findall(f".//{{{namespace}}}{parent_dom}")
                for item in items:
                    i += 1
                    try:
                        code = item.find(f".//{{{namespace}}}code").text
                        name = item.find(f".//{{{namespace}}}name").text
                        parent = item.find(f".//{{{namespace}}}parentCode").text if item.find(
                            f".//{{{namespace}}}parentCode") is not None else None
                        nsiOktmo.objects.get_or_create(
                            code=code,
                            name=name,
                            parent=parent,
                        )
                    except Exception as e:
                        pass
                    if i > self.limit_record:
                        br = True
                        break
            if br:
                break

            if class_name == 'nsiOkopf':
                namespace = "http://zakupki.gov.ru/223fz/reference/1"
                parent_dom = "nsiOkopfData"

                items = root.findall(f".//{{{namespace}}}{parent_dom}")
                for item in items:
                    i += 1
                    try:
                        code = item.find(f".//{{{namespace}}}code").text
                        name = item.find(f".//{{{namespace}}}name").text
                        nsiOkopf.objects.get_or_create(
                            code=code,
                            name=name,
                        )
                    except Exception as e:
                        pass
                    if i > self.limit_record:
                        br = True
                        break
            if br:
                break

            if class_name == 'nsiOkved':
                namespace = "http://zakupki.gov.ru/223fz/reference/1"
                parent_dom = "nsiOkvedData"

                items = root.findall(f".//{{{namespace}}}{parent_dom}")
                for item in items:
                    i += 1
                    try:
                        code = item.find(f".//{{{namespace}}}code").text
                        name = item.find(f".//{{{namespace}}}name").text
                        section = item.find(f".//{{{namespace}}}section").text
                        parent = item.find(f".//{{{namespace}}}parentCode").text if item.find(
                            f".//{{{namespace}}}parentCode") is not None else None
                        nsiOkved.objects.get_or_create(
                            code=code,
                            name=name,
                            section=section,
                            parent=parent,
                        )
                    except Exception as e:
                        pass
                    if i > self.limit_record:
                        br = True
                        break
            if br:
                break

            if class_name == 'nsiOkved2':
                namespace = "http://zakupki.gov.ru/223fz/reference/1"
                parent_dom = "nsiOkved2Data"

                items = root.findall(f".//{{{namespace}}}{parent_dom}")
                for item in items:
                    i += 1
                    try:
                        code = item.find(f".//{{{namespace}}}code").text
                        name = item.find(f".//{{{namespace}}}name").text
                        section = item.find(f".//{{{namespace}}}section").text
                        parent = item.find(f".//{{{namespace}}}parentCode").text if item.find(
                            f".//{{{namespace}}}parentCode") is not None else None
                        nsiOkved2.objects.get_or_create(
                            code=code,
                            name=name,
                            section=section,
                            parent=parent,
                        )
                    except Exception as e:
                        pass
                    if i > self.limit_record:
                        br = True
                        break
            if br:
                break

            if class_name == 'nsiOkv':
                namespace = "http://zakupki.gov.ru/223fz/reference/1"
                parent_dom = "nsiOkvData"

                items = root.findall(f".//{{{namespace}}}{parent_dom}")
                for item in items:
                    i += 1
                    try:
                        code = item.find(f".//{{{namespace}}}code").text
                        digitalCode = item.find(f".//{{{namespace}}}digitalCode").text
                        name = item.find(f".//{{{namespace}}}name").text
                        shortName = item.find(f".//{{{namespace}}}shortName").text
                        nsiOkv.objects.get_or_create(
                            code=code,
                            name=name,
                            digitalCode=digitalCode,
                            shortName=shortName,
                        )
                    except Exception as e:
                        pass
                    if i > self.limit_record:
                        br = True
                        break
            if br:
                break

            if class_name == 'nsiOrganization':
                namespace = "http://zakupki.gov.ru/223fz/reference/1"
                parent_dom = "nsiOrganizationData"

                items = root.findall(f".//{{{namespace}}}{parent_dom}")
                for item in items:
                    i += 1
                    try:
                        full_name = item.find(f".//{{{namespace}}}mainInfo")[0].text
                        short_name = item.find(f".//{{{namespace}}}mainInfo")[1].text
                        registration_date = item.find(f".//{{{namespace}}}codeAssignDateTime").text
                        ogrn = item.find(f".//{{{namespace}}}mainInfo")[4].text
                        inn = item.find(f".//{{{namespace}}}mainInfo")[2].text
                        kpp = item.find(f".//{{{namespace}}}mainInfo")[3].text
                        legalAddress = item.find(f".//{{{namespace}}}mainInfo")[5].text
                        postalAddress = item.find(f".//{{{namespace}}}mainInfo")[6].text
                        timeZone, cr = nsiTimeZone.objects.get_or_create(
                            offset=item.find(f".//{{{namespace}}}additionalInfo").find(
                                f".//{{{namespace}}}timeZone").find(f".//{{{namespace}}}offset").text,
                            name=item.find(f".//{{{namespace}}}additionalInfo").find(
                                f".//{{{namespace}}}timeZone").find(f".//{{{namespace}}}name").text,
                        )
                        okpo, cr = nsiOkpo.objects.get_or_create(
                            code=item.find(f".//{{{namespace}}}classification").find(f".//{{{namespace}}}okpo").text,
                        )
                        okato, cr = nsiOkato.objects.get_or_create(
                            code=item.find(f".//{{{namespace}}}classification").find(f".//{{{namespace}}}okato").text,
                        )
                        oktmo, cr = nsiOktmo.objects.get_or_create(
                            code=item.find(f".//{{{namespace}}}classification").find(f".//{{{namespace}}}oktmo").text,
                        )
                        okfs, cr = nsiOkfs.objects.get_or_create(
                            code=item.find(f".//{{{namespace}}}classification").find(f".//{{{namespace}}}okfs").text,
                        )
                        okopf, cr = nsiOkopf.objects.get_or_create(
                            code=item.find(f".//{{{namespace}}}classification").find(f".//{{{namespace}}}okopf").text,
                        )

                        org, cr = Organization.objects.get_or_create(
                            full_name=full_name,
                            short_name=short_name,
                            registration_date=registration_date,
                            ogrn=ogrn,
                            inn=inn,
                            kpp=kpp,
                            legalAddress=legalAddress,
                            postalAddress=postalAddress,
                            timeZone=timeZone,
                            okpo=okpo,
                            okato=okato,
                            oktmo=oktmo,
                            okfs=okfs,
                            okopf=okopf,
                        )

                    except Exception as e:
                        pass

                    try:
                        root = item.find(f".//{{{namespace}}}classification").find(
                            f".//{{{namespace}}}activities")
                        okvs = root.findall(f".//{{{namespace}}}okved")
                        for okv in okvs:
                            o_okv, cr = nsiOkved.objects.get_or_create(
                                code=okv.find(f".//{{{namespace}}}code").text,
                                name=okv.find(f".//{{{namespace}}}name").text
                            )
                            is_main = bool(okv.find(f".//{{{namespace}}}isMain").text)
                            OrganizationOkved.objects.get_or_create(
                                isMain=is_main,
                                organization=org,
                                okved=o_okv,
                            )
                    except Exception as e:
                        pass

                    try:
                        root = item.find(f".//{{{namespace}}}classification").find(
                            f".//{{{namespace}}}activities")
                        okvs = root.findall(f".//{{{namespace}}}okved2")
                        for okv in okvs:
                            o_okv, cr = nsiOkved2.objects.get_or_create(
                                code=okv.find(f".//{{{namespace}}}code").text,
                                name=okv.find(f".//{{{namespace}}}name").text
                            )
                            is_main = bool(okv.find(f".//{{{namespace}}}isMain").text)
                            OrganizationOkved2.objects.get_or_create(
                                isMain=is_main,
                                organization=org,
                                okved2=o_okv,
                            )
                    except Exception as e:
                        pass

                    if i > self.limit_record:
                        br = True
                        break
            if br:
                break


    def remove_files(self, files):
        for file in files:
            os.remove(file)
    def parse_model(self, model):
        model = f"{model[:3]}{model[3].upper()}{model[4:]}"
        print(model)
        files = self.get_xml_files(f"/out/nsi/{model}")
        self.parse_and_save_to_db(model, files)
        self.remove_files(files)

    def parse_nsiOkato(self):
        files = self.get_xml_files("/out/nsi/nsiOkato")
        self.parse_and_save_to_db('nsiOkato', files)
        self.remove_files(files)

    def parse_nsiOkdp(self):
        files = self.get_xml_files("/out/nsi/nsiOkdp")
        self.parse_and_save_to_db('nsiOkdp', files)
        self.remove_files(files)

    def parse_nsiOkdp2(self):
        files = self.get_xml_files("/out/nsi/nsiOkpd2")
        self.parse_and_save_to_db('nsiOkpd2', files)
        self.remove_files(files)

    def parse_nsiOkei(self):
        files = self.get_xml_files("/out/nsi/nsiOkei")
        self.parse_and_save_to_db('nsiOkei', files)
        self.remove_files(files)

    def parse_nsiOkfs(self):
        files = self.get_xml_files("/out/nsi/nsiOkfs")
        self.parse_and_save_to_db('nsiOkfs', files)
        self.remove_files(files)

    def parse_nsiOkogu(self):
        files = self.get_xml_files("/out/nsi/nsiOkogu")
        self.parse_and_save_to_db('nsiOkogu', files)
        self.remove_files(files)

    def parse_nsiOktmo(self):
        files = self.get_xml_files("/out/nsi/nsiOktmo")
        self.parse_and_save_to_db('nsiOktmo', files)
        self.remove_files(files)

    def parse_nsiOkopf(self):
        files = self.get_xml_files("/out/nsi/nsiOkopf")
        self.parse_and_save_to_db('nsiOkopf', files)
        self.remove_files(files)

    def parse_nsiOkved(self):
        files = self.get_xml_files("/out/nsi/nsiOkved")
        self.parse_and_save_to_db('nsiOkved', files)
        self.remove_files(files)

    def parse_nsiOkved2(self):
        files = self.get_xml_files("/out/nsi/nsiOkved2")
        self.parse_and_save_to_db('nsiOkved2', files)
        self.remove_files(files)

    def parse_nsiOkv(self):
        files = self.get_xml_files("/out/nsi/nsiOkv")
        self.parse_and_save_to_db('nsiOkv', files)
        self.remove_files(files)

    def parse_Organization(self):
        files = self.get_xml_files("/out/nsi/nsiOrganization")
        self.parse_and_save_to_db('nsiOrganization', files)
        self.remove_files(files)


@shared_task
def download(model):
    zp = ZakupkiParser()
    if model[:3] == 'nsi':
        zp.parse_model(model)
    else:
        zp.parse_Organization()

@shared_task
def get_query_from_rts():
    nsiOkpd2 = apps.get_model('main_app', 'nsiOkpd2')
    nsiOkei = apps.get_model('main_app', 'nsiOkei')
    Query = apps.get_model('main_app', 'Query')
    Organization = apps.get_model('main_app', 'Organization')
    Nomenclature = apps.get_model('main_app', 'Nomenclature')
    QueryNomenclature = apps.get_model('main_app', 'QueryNomenclature')
    base_url = 'https://www.rosatom.rts-tender.ru'
    url = f"{base_url}/market/?searching=1&company_type=2&price_currency=0&guarantee_currency=0&date=1&trade=buy&lot_type=38#search-result"
    s = requests.session()
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # считываем первую страницу
    for item in soup.select('a.search-results-title'):

        item_link = item.get('href')
        r = s.get(item_link)
        soup_item = BeautifulSoup(r.text, 'html.parser')
        okpd2s = soup_item.select('tr#trade-info-okpd2 td:last-child div.expandable-text.full')
        if len(okpd2s) == 0:
            okpd2s = soup_item.select('tr#trade-info-okpd2 td:last-child div')
        for i, okpd2_t in enumerate(okpd2s):
            okpd2_code = soup_item.select('tr#trade-info-okpd2 td:last-child div b')[i].text
            okpd2_text = re.sub(r'[\d]*[<>/b.]*','', okpd2_t.text).strip()
            okpd2, c = nsiOkpd2.objects.get_or_create(code=okpd2_code, name=okpd2_text)
            okpd2.save()
        org_link = f"{base_url}{soup_item.select('tr#trade-info-organizer-name td:last-child a')[0].get('href')}"
        r = s.get(org_link)
        soup_org = BeautifulSoup(r.text, 'html.parser')
        print(org_link)
        short = soup_org.select('td.small')[0].parent.select('td:last-child')[0].text
        full = soup_org.select('td.small')[1].parent.select('td:last-child')[0].text
        inn = soup_org.select('td.small')[2].parent.select('td:last-child')[0].text
        if len(soup_org.select('td.small')) > 3:
            kpp = soup_org.select('td.small')[3].parent.select('td:last-child')[0].text
            ogrn = soup_org.select('td.small')[5].parent.select('td:last-child')[0].text
        else:
            kpp = ''
            ogrn = ''
        if len(inn) > 20:
            inn = ''
        org, c = Organization.objects.get_or_create(
            short_name=short,
            full_name=full,
            inn=inn,
            kpp=kpp,
            ogrn=ogrn,
        )
        org.save()
        date_begin = soup_item.select('tr#trade_info_date_begin td:last-child span')[0].get('content')
        date_end =soup_item.select('tr#trade_info_date_end td:last-child')[0].text[:10]
        desc = soup_item.find_all(attrs={"itemprop": "articleBody"})[0].text
        num = soup_item.find_all(attrs={"itemprop": "headline"})[0].text
        num =  re.findall(r'\d+', num)[0]
        q, c = Query.objects.get_or_create(
            okpd2=okpd2,
            organizer=org,
            description=desc,
            num=num,
            date_begin=date_begin,
            date_end=f"{date_end[6:]}-{date_end[3:5]}-{date_end[0:2]}",
            link_to_doc=item_link,
        )
        q.save()
        nomen_link = f"{base_url}{soup_item.select('div.nav-pills ul li:last-child a ')[0].get('href')}"
        r = s.get(nomen_link)
        soup_nomen =BeautifulSoup(r.text, 'html.parser')
        names = soup_nomen.select('div.wideTable-wrap tr:not(.thead) td:nth-child(2)')
        counts = soup_nomen.select('div.wideTable-wrap tr:not(.thead) td:nth-child(8)')
        eis = soup_nomen.select('div.wideTable-wrap tr:not(.thead) td:nth-child(9)')
        for i, name in enumerate(names):
            ei, c = nsiOkei.objects.get_or_create(name=eis[i].text)
            ei.save()
            nom, c = Nomenclature.objects.get_or_create(name=name.text)
            nom.save()
            nom_query, c = QueryNomenclature.objects.get_or_create(
                nomenclature=nom,
                count=counts[i].text,
                ei=ei,
                query=q,
            )
            nom_query.save()
    pages = soup.select('li.pagi-item > a')
    for page in pages:
        page_url = f"{base_url}{page.get('href')}"
        r = s.get(page_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for item in soup.select('a.search-results-title'):
            item_link = item.get('href')
            r = s.get(item_link)
            soup_item = BeautifulSoup(r.text, 'html.parser')
            okpd2s = soup_item.select('tr#trade-info-okpd2 td:last-child div.expandable-text.full')
            if len(okpd2s) == 0:
                okpd2s = soup_item.select('tr#trade-info-okpd2 td:last-child div')
            for i, okpd2_t in enumerate(okpd2s):
                okpd2_code = soup_item.select('tr#trade-info-okpd2 td:last-child div b')[i].text
                okpd2_text = re.sub(r'[\d]*[<>/b.]*','', okpd2_t.text).strip()
                okpd2, c = nsiOkpd2.objects.get_or_create(code=okpd2_code, name=okpd2_text)
                okpd2.save()
            org_link = f"{base_url}{soup_item.select('tr#trade-info-organizer-name td:last-child a')[0].get('href')}"
            r = s.get(org_link)
            soup_org = BeautifulSoup(r.text, 'html.parser')
            print(org_link)
            short = soup_org.select('td.small')[0].parent.select('td:last-child')[0].text
            full = soup_org.select('td.small')[1].parent.select('td:last-child')[0].text
            inn = soup_org.select('td.small')[2].parent.select('td:last-child')[0].text
            if len(soup_org.select('td.small')) > 3:
                kpp = soup_org.select('td.small')[3].parent.select('td:last-child')[0].text
                ogrn = soup_org.select('td.small')[5].parent.select('td:last-child')[0].text
            else:
                kpp = ''
                ogrn = ''
            if len(inn) > 20:
                inn = ''
            org, c = Organization.objects.get_or_create(
                short_name=short,
                full_name=full,
                inn=inn,
                kpp=kpp,
                ogrn=ogrn,
            )
            org.save()
            date_begin = soup_item.select('tr#trade_info_date_begin td:last-child span')[0].get('content')
            date_end =soup_item.select('tr#trade_info_date_end td:last-child')[0].text[:10]
            desc = soup_item.find_all(attrs={"itemprop": "articleBody"})[0].text
            num = soup_item.find_all(attrs={"itemprop": "headline"})[0].text
            num =  re.findall(r'\d+', num)[0]
            q, c = Query.objects.get_or_create(
                okpd2=okpd2,
                organizer=org,
                description=desc,
                num=num,
                date_begin=date_begin,
                date_end=f"{date_end[6:]}-{date_end[3:5]}-{date_end[0:2]}",
                link_to_doc=item_link,
            )
            q.save()
            nomen_link = f"{base_url}{soup_item.select('div.nav-pills ul li:last-child a ')[0].get('href')}"
            r = s.get(nomen_link)
            soup_nomen =BeautifulSoup(r.text, 'html.parser')
            names = soup_nomen.select('div.wideTable-wrap tr:not(.thead) td:nth-child(2)')
            counts = soup_nomen.select('div.wideTable-wrap tr:not(.thead) td:nth-child(8)')
            eis = soup_nomen.select('div.wideTable-wrap tr:not(.thead) td:nth-child(9)')
            for i, name in enumerate(names):
                ei, c = nsiOkei.objects.get_or_create(name=eis[i].text)
                ei.save()
                nom, c = Nomenclature.objects.get_or_create(name=name.text)
                nom.save()
                nom_query, c = QueryNomenclature.objects.get_or_create(
                    nomenclature=nom,
                    count=counts[i].text,
                    ei=ei,
                    query=q,
                )
                nom_query.save()

