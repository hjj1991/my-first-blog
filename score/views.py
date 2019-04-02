from django.shortcuts import render
import requests, json

# Create your views here.

#League of Legends 전적검색
def score_view(request):
    return render(request, 'score/score_view.html')

def search_result(request):
	if request.method == "GET":
		summoner_name = request.GET.get('search_text')

		sum_result = {}
		solo_tier = {}
		team_tier = {}
		store_list = []
		game_list ={}
		game_list2 = []


		summoner_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summoner_name)	#소환사 정보 검색
		params = {'api_key': 'RGAPI-00acf972-10de-4381-8a1c-4c41b0cf7692'}
		res = requests.get(summoner_url, params=params)
		summoners_result = json.loads(((res.text).encode('utf-8')))
		if summoners_result:
			sum_result['name'] = summoners_result['name']
			sum_result['level'] = summoners_result['summonerLevel']
			sum_result['profileIconId'] = summoners_result['profileIconId']

			game_url = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoners_result['accountId']	#최근 10경기 정보
			params1 = {'api_key': 'RGAPI-00acf972-10de-4381-8a1c-4c41b0cf7692', 'endIndex':'10'}
			game_list = requests.get(game_url, params=params1)
			game_list = json.loads(((game_list.text).encode('utf-8')))
			game_list = game_list['matches']
			if len(game_list) > 1:
				for item in game_list:
					game_list2.append(item)




			tier_url = "https://kr.api.riotgames.com/lol/league/v4/positions/by-summoner/" + summoners_result['id']	#소환사 티어 검색
			tier_info = requests.get(tier_url, params=params)
			tier_info = json.loads(((tier_info.text).encode('utf-8')))

			# solo_tier = len(tier_info)
			# tier_info = tier_info.pop()
			# solo_tier['rank_type'] = '솔로랭크 5:5'
			# solo_tier['losses'] = tier_info['losses']
			if len(tier_info) == 1:
				tier_info = tier_info.pop()
				if tier_info['queueType'] == 'RANKED_FLEX_SR':
					team_tier['rank_type'] = '자유랭크 5:5'
					team_tier['tier'] = tier_info['tier']
					team_tier['rank'] = tier_info['rank']
					team_tier['points'] = tier_info['leaguePoints']
					team_tier['wins'] = tier_info['wins']
					team_tier['losses'] = tier_info['losses']
				else:
					solo_tier['rank_type'] = '솔로랭크 5:5'
					solo_tier['tier'] = tier_info['tier']
					solo_tier['rank'] = tier_info['rank']
					solo_tier['points'] = tier_info['leaguePoints']
					solo_tier['wins'] = tier_info['wins']
					solo_tier['losses'] = tier_info['losses']		
			if len(tier_info) == 2:
				for item in tier_info:
					store_list.append(item)
				solo_tier['rank_type'] = '솔로랭크 5:5'
				solo_tier['tier'] = store_list[1]['tier']
				solo_tier['rank'] = store_list[1]['rank']
				solo_tier['points'] = store_list[1]['leaguePoints']
				solo_tier['wins'] = store_list[1]['wins']
				solo_tier['losses'] = store_list[1]['losses']

				team_tier['rank_type'] = '자유랭크 5:5'
				team_tier['tier'] = store_list[0]['tier']
				team_tier['rank'] = store_list[1]['rank']
				team_tier['points'] = store_list[0]['leaguePoints']
				team_tier['wins'] = store_list[0]['wins']
				team_tier['losses'] = store_list[0]['losses']				




		return render (request, 'score/search_result.html', {'summoners_result': sum_result, 'solo_tier': solo_tier, 'team_tier': team_tier, 'game_list2': game_list2})
