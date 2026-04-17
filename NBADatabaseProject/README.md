# Purpose
My first simple analysis revolved around correlating height and position, but I wanted to do someething bigger for the second analysis. After looking at the data for a bit, I decided to create a set of csv files to use with Tableau to create a dashboard to look over the NBA from 1996 to 2022. Although, I wanted to look at personnel, league, team, and game data, it became clear with enough exploration that the database wasn't fit for anything but team or game analysis. Unofortunately, the database is mostly dedicated to play-by-play anmd game data for games, and has limited data for players and teams to the point that getting the career stats for a player would require stitching it together from play-by-play data. Stitching together team data is much less daunting so that is the path I took for this round of analysis.

Originally, I intended to include postseason and preseaon analysis but there are too few games in the preseason and the postseason is too sporadic. A team maybe play only four games because they get swept in the playoffs and never reach the postseason for years. That sort of data may make it difficult to get any meaningful distinctions or conclusions. Right now, the analysis is solely for the regular season.

The general plan is to create a dashboard via Tableau that showcases the stats of a team over time, and showcases the strengths of a team during a period of seasons.

# Process

I want to fetch field goals attemped and made, 3-point field goals attempted and made, free throws attempted and made, offensive/defensive/total rebounds, assists, steals, blocks, turnovers, personal fouls, plus-minus and points for each team from the game table, averaging it for each season, and divided up by pre-season, the season itself, and the playoffs. From the other_stats table, I want to fetch points in the paint, points off turnovers, second chance and fastbreak points. From team_info_common, I want to fetch the team's conference and division, and their ranks within each during each season.

The team's win-loss will be fetched by 

## Derived Statistics
The NBA has a [page about advanced statistics](https://www.nba.com/stats/teams/advanced) which details a few statistics to calculate: offensive and defensive rating, among others which I will try to calculate. They also have a [page about miscellaneous statistics](https://www.nba.com/stats/teams/misc), all of which are supposed to be found in the other_stats table, but for whatever reason the table is empty in what I downloaded. I will try to calculate as much of these as possible but the miscelleanous stats probably need to be scraped from the website.

## Organization

For Tableau, all data needs to be a in a single file, but for a database, it can be divided up so each team (and the league itself) gets its own table.

# Conclusion
The [Tableau dashboard](https://public.tableau.com/app/profile/kacper.sienkiewicz/viz/NBATeamComparison_17764643705190/Overview) was created, and although it is a bit sluggish it was a success. 
