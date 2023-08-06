from ..sessioncontroll import baseobj, strobj, baseobj, floatobj, colobj, fkyobj


class CalculatedScoreData(baseobj):
    __tablename__ = "calculated_score"
    racehorsekey = colobj(strobj, fkyobj("racehorse.racehorsekey"), primary_key=True)
    waku_win_rate = colobj(floatobj)
    waku_rentai_rate = colobj(floatobj)
