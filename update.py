import json
from datetime import datetime,timezone,timedelta
import pandas as pd
import yfinance as yf
JST=timezone(timedelta(hours=9))
TICKERS={"7203":"トヨタ自動車","6758":"ソニーグループ","9984":"ソフトバンクグループ","8035":"東京エレクトロン","6857":"アドバンテスト","6920":"レーザーテック","6146":"ディスコ","7735":"SCREENホールディングス","6723":"ルネサスエレクトロニクス","4063":"信越化学工業","6981":"村田製作所","6976":"太陽誘電","6762":"TDK","6501":"日立製作所","6503":"三菱電機","6506":"安川電機","6954":"ファナック","6594":"ニデック","5803":"フジクラ","5802":"住友電気工業","5401":"日本製鉄","5713":"住友金属鉱山","5016":"JX金属","8031":"三井物産","8002":"丸紅","8001":"伊藤忠商事","8058":"三菱商事","8053":"住友商事","9432":"NTT","9433":"KDDI","9983":"ファーストリテイリング","6098":"リクルートホールディングス","6367":"ダイキン工業","6301":"コマツ","6305":"日立建機","7267":"ホンダ","7269":"スズキ","6902":"デンソー","6988":"日東電工","6861":"キーエンス","7733":"オリンパス","4519":"中外製薬","4568":"第一三共","4502":"武田薬品工業","4503":"アステラス製薬","3382":"セブン&アイ・ホールディングス","9843":"ニトリホールディングス","9989":"サンドラッグ","2914":"JT","8766":"東京海上ホールディングス","8316":"三井住友FG","8306":"三菱UFJ FG","8411":"みずほFG","8604":"野村HD","8591":"オリックス","8750":"第一生命HD","8801":"三井不動産","8802":"三菱地所","9020":"JR東日本","9022":"JR東海","9101":"日本郵船","9104":"商船三井","9107":"川崎汽船","9501":"東京電力HD","9502":"中部電力","9531":"東京ガス","8056":"BIPROGY","9434":"ソフトバンク","4689":"LINEヤフー","2413":"エムスリー"}
def dl(sym,period="3mo"):
    try:return yf.download(sym+".T",period=period,interval="1d",auto_adjust=True,progress=False,threads=False)
    except:return pd.DataFrame()
def sig(sym):
    try:
        d=yf.download(sym,period="1mo",interval="1d",auto_adjust=True,progress=False,threads=False);c=d["Close"].dropna()
        c=d["Close"].dropna()
        if len(c)<5:return 0,"--"
        r=(float(c.iloc[-1])/float(c.iloc[-2])-1)*100
        return max(-2,min(2,r*1.2)),f"{r:+.1f}%"
    except:return 0,"--"
def main():
    sp,spt=sig("^GSPC");nd,ndt=sig("^IXIC");dj,djt=sig("^DJI");sox,soxt=sig("^SOX")
    us=(sp+nd+dj)/3
    rows=[]
    for code,name in TICKERS.items():
        d=dl(code)
        if d.empty or len(d)<
        c=d["Close"].dropna()
        c=c.iloc[:,0] if hasattr(c,"columns") else c
        r5=(p/p5-1)*100;ma5=float(c.tail(5).mean());ma20=float(c.tail(20).mean());vr=float(v.tail(5).mean()/v.tail(20).mean()) if float(v.tail(20).mean())else 1
        trend=1 if p>ma5>ma20 else (0.5 if p>ma20 else 0)
        mom=max(0,min(1,(r5+5)/15));vol=max(0,min(1,(vr-.8)/1.7));mk=max(0,min(1,(us+2)/4));sb=max(0,min(1,(sox+2)/4))
        score=100*(.30*trend+.28*mom+.18*vol+.14*mk+.10*sb)
        if score<35:continue
        rs=[]
        if trend>=1:rs.append("5日線＞20日線")
        elif p>ma20:rs.append("20日線を上回る")
        if r5>2:rs.append(f"5日騰落率 {r5:+.1f}%")
        if vr>1.2:rs.append(f"出来高増加{vr:.1f}倍")
        if us>.35:rs.append("米国株が追い風")
        if sox>.5 and code in {"8035","6857","6920","6146","7735","6723","4063","6981","6976","6762"}:rs.append("半導体地合いが追い風")
        if not rs:rs.append("複数のテクニカル条件が改善")
        rows.append({"code":code,"name":name,"price":round(p,1),"score":round(score,1),"signal":"監視候補","reason":"、".join(rs)})
    rows=sorted(rows,key=lambda x:x["score"],reverse=True)[:20]
    out={"asof_jst":datetime.now(JST).strftime("%Y-%m-%d %H:%M JST"),"market_summary":f"S&P500{spt}/Nasdaq{ndt}/Dow{djt}/SOX{soxt}","us_signal":"追い風" if us>.35 else ("向かい風" if us<-.35 else "中立"),"jp_signal":"前日終値ベース","semi_signal":"強い" if sox>.5 else ("弱い" if sox<-.5 else "中立"),"stocks":rows}
    json.dump(out,open("data.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
if __name__=="__main__":main()
