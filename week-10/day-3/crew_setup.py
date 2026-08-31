# make_researcher()               an Agent with the city_info tool
# make_analyst()                  an Agent with calculate and word_count
# make_tasks(researcher, analyst) two Tasks - find a fact, then use it
# build_crew()                    a sequential Crew with both agents and tasks
# describe_crew(crew)             "2 agents (Researcher, Analyst), 2 tasks, sequential"
#
# Every agent needs role, goal, and a backstory of at least twelve words.
# Every task needs an expected_output. Those fields ARE the prompt.
#
# from crewai import Agent, Task, Crew, Process
