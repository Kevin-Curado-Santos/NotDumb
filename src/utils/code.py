import requests
import discord
import random
import json

from discord.ext import commands 

problemset_api = "https://codeforces.com/api/problemset.problems"
problemset_url = "https://codeforces.com/problemset/problem"

def check_problem(rating):
    return (lambda problem: "contestId" in problem and "rating" in problem and problem["rating"] >= rating[0] and problem["rating"] <= rating[1])

def get_random_problem(problems):
    random_problem_index = random.randint(0, len(problems) - 1)
    random_problem = problems[random_problem_index]
    return random_problem

def process_response(request):
    result = request.text
    result = json.loads(result)
    problems = result["result"]["problems"]
    return problems

class Codebot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def problem(self, ctx, *, tags = ""):
        rating = (0, 10000)
        tags = tags.split(',')
        problem_tags = []

        for t in tags:
            if t == "":
                pass
            elif '~' in t:
                [l, r] = t.split('~')
                l = int(l) if l != '' else 0
                r = int(r) if r != '' else 0
                rating = (l, r)
            elif t[0] == '-':
                pass
                # special tags
            else:
                problem_tags.append(t)

        query_url = problemset_api
        if len(problem_tags) > 0:
            query_url += f"?tags={';'.join(problem_tags)}"

        request = requests.get(query_url)
        problems = process_response(request)
        problems = list(filter(check_problem(rating), problems))
        if len(problems) == 0:
            await ctx.send("Could not find such a problem")
            return 

        random_problem = get_random_problem(problems)

        problem_url = problemset_url
        problem_url += f"/{random_problem["contestId"]}"
        problem_url += f"/{random_problem["index"]}"
        
        emb = discord.Embed(title = random_problem["name"])
        emb.add_field(name=problem_url, value = '')
        emb.add_field(name="Tags", value=', '.join(random_problem["tags"] + [str(random_problem["rating"])] if "rating" in random_problem else []))

        await ctx.send(embed = emb)





