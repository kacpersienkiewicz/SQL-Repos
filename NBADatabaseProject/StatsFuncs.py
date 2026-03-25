'''
This file has two functions:
* import all needed modules so just this file can be imported
* create a bunch of helper functions for analysis, mainly for calculating advanced stats like PER

'''
import sqlite3 as sql
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def get_uPER(player_stats, team_stats, league_stats):
    '''
    https://www.basketball-reference.com/about/per.html
    Given a player's stats, and a season (used to calculate team and league stats) spits out a PER, which biases towards offensives stats.
    lg - > league, tm -> team
    mp = minutes played
    pts = points
    ast = assists
    rb = rebounds
    orb = offensive rebounds
    drb = defensive rebounds
    trb = total rebounds
    stl = steals
    blk = blocks
    tov = turnovers
    pf = personal fouls
    fg = field goal made
    fga = field goals attempted
    fg3 = 3-point field goals
    ft = free throws
    factor = arbitrary factor?
    vop = value of possession
    drbp = defensive rebound percentage
    '''
    name, mp, pts, ast, trb, orb, drb, stl, blk, tov, pf, fg, fga, fg3, fg3a, ft, fta  = player_stats # Not all will be used but this is the standard stat array
    team, tm_pts, tm_ast, tm_trb, tm_orb, tm_drb, tm_stl, tm_blk, tm_tov, tm_pf, tm_fg, tm_fga, tm_fg3, tm_fg3a, tm_ft, tm_fta  = team_stats
    season, lg_pts, lg_ast, lg_trb, lg_orb, lg_drb, lg_stl, lg_blk, lg_tov, lg_pf, lg_fg, lg_fga, lg_fg3, lg_fg3a, lg_ft, lg_fta = league_stats
    
    factor = (2 / 3) - (0.5 * (lg_ast / lg_fg) / (2 * (lg_fg / lg_ft)))
    vop = lg_pts / (lg_fga - lg_orb + lg_tov + (0.44 * lg_fta))
    drbp = (lg_trb - lg_orb) / lg_trb

    uPER = 1 / mp * (fg3 + (2/3) * ast + (2 - factor * (tm_ast / tm_fg)) * fg \
                    + (ft * 0.5 * (1 + (1 - (tm_ast / tm_fg)) + 2/3 * (tm_ast / tm_fg))) \
                    - vop * tov - vop * drbp * (fga - fg) \
                    - vop * (0.44  * (0.44 + (0.56 * drbp)) * (fta - ft)) \
                    + vop * (1 - drbp) * (trb - orb) + vop * drbp * orb + vop * stl + vop * drbp * blk \
                    - pf * ((lg_ft / lg_pf) - 0.44 * (lg_fta / lg_pf) * vop))
    
    return uPER

def get_aPER(uPER, pace_adjustment):
    # PER is typically adjusted by pace. Basketball Reference has a pace adjustment of league pace / team pace
    # priot to 1973-1974, Basketball Reference uses the following: estimated pace adjustment = 2 * lg_PPG / (tm_PPG + opp_PPG)
    # pace is 48 * (tm_poss + opp_poss) / (2 * (tm_mp/5)), and it estimates possessions per 48 minutes
    return pace_adjustment * uPER

def get_PER(aPER, lg_aPER):
    # Basetball Reference also adjusts per a league average adjusted per over 15 seasons, which is also done here
    return  aPER * (15 / lg_aPER)

def calc_pace_adjustment(lg_pace, tm_pace):
    return lg_pace / tm_pace

def estimate_pace_adjustment(lg_ppg, tm_ppg, opp_ppg):
    return 2 * lg_ppg / (tm_ppg * opp_ppg)

def calc_lg_aPER():
    #wip
    return 
