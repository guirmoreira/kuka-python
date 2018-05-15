import xml.etree.cElementTree as Xml
from models import Coordinates, Axes, Data


def generate_receive_xml(pos, dig, ipoc):
    xml = Xml.parse('receive.xml')
    root = xml.getroot()
    root[1].set('X', '%.4f' % round(pos.x, 4))
    root[1].set('Y', '%.4f' % round(pos.y, 4))
    root[1].set('Z', '%.4f' % round(pos.z, 4))
    root[1].set('A', '%.4f' % round(pos.a, 4))
    root[1].set('B', '%.4f' % round(pos.b, 4))
    root[1].set('C', '%.4f' % round(pos.c, 4))
    # todo future implementations for other corrections
    root[5].set('D1', '%d' % dig.o1)
    root[5].set('D2', '%d' % dig.o2)
    root[5].set('D3', '%d' % dig.o3)
    root[6].text = str(ipoc)
    xml.write('receive_mod.xml')
    xml_bytes = Xml.tostring(root)
    return xml_bytes


def get_data_from_send_xml(root):

    r_ist = Coordinates(x=float(root.find('RIst').get('X')), y=float(root.find('RIst').get('Y')),
                        z=float(root.find('RIst').get('Z')),
                        a=float(root.find('RIst').get('A')), b=float(root.find('RIst').get('B')),
                        c=float(root.find('RIst').get('C')))

    r_sol = Coordinates(x=float(root.find('RSol').get('X')), y=float(root.find('RSol').get('Y')),
                        z=float(root.find('RSol').get('Z')),
                        a=float(root.find('RSol').get('A')), b=float(root.find('RSol').get('B')),
                        c=float(root.find('RSol').get('C')))

    ai_pos = Axes(a1=float(root.find('AIPos').get('A1')), a2=float(root.find('AIPos').get('A2')),
                  a3=float(root.find('AIPos').get('A3')),
                  a4=float(root.find('AIPos').get('A4')), a5=float(root.find('AIPos').get('A5')),
                  a6=float(root.find('AIPos').get('A6')))

    as_pos = Axes(a1=float(root.find('ASPos').get('A1')), a2=float(root.find('ASPos').get('A2')),
                  a3=float(root.find('ASPos').get('A3')),
                  a4=float(root.find('ASPos').get('A4')), a5=float(root.find('ASPos').get('A5')),
                  a6=float(root.find('ASPos').get('A6')))

    ei_pos = Axes(a1=float(root.find('EIPos').get('E1')), a2=float(root.find('EIPos').get('E2')),
                  a3=float(root.find('EIPos').get('E3')),
                  a4=float(root.find('EIPos').get('E4')), a5=float(root.find('EIPos').get('E5')),
                  a6=float(root.find('EIPos').get('E6')))

    es_pos = Axes(a1=float(root.find('ESPos').get('E1')), a2=float(root.find('ESPos').get('E2')),
                  a3=float(root.find('ESPos').get('E3')),
                  a4=float(root.find('ESPos').get('E4')), a5=float(root.find('ESPos').get('E5')),
                  a6=float(root.find('ESPos').get('E6')))

    ma_cur = Axes(a1=float(root.find('MACur').get('A1')), a2=float(root.find('MACur').get('A2')),
                  a3=float(root.find('MACur').get('A3')),
                  a4=float(root.find('MACur').get('A4')), a5=float(root.find('MACur').get('A5')),
                  a6=float(root.find('MACur').get('A6')))

    me_cur = Axes(a1=float(root.find('MECur').get('E1')), a2=float(root.find('MECur').get('E2')),
                  a3=float(root.find('MECur').get('E3')),
                  a4=float(root.find('MECur').get('E4')), a5=float(root.find('MECur').get('E5')),
                  a6=float(root.find('MECur').get('E6')))

    delay = int(root.find('Delay').get('D'))

    ftc = Coordinates(x=float(root.find('FTC').get('Fx')), y=float(root.find('FTC').get('Fy')),
                      z=float(root.find('FTC').get('Fz')),
                      a=float(root.find('FTC').get('Mz')), b=float(root.find('FTC').get('My')),
                      c=float(root.find('FTC').get('Mx')))

    ipoc = int(root.find('IPOC').text)

    data = Data(r_ist=r_ist, r_sol=r_sol, ai_pos=ai_pos, as_pos=as_pos, ei_pos=ei_pos, es_pos=es_pos, ma_cur=ma_cur,
                me_cur=me_cur, delay=delay, ftc=ftc, ipoc=ipoc)

    return data
