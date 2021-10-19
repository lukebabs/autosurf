import os, random

def get_user_agents():
        with open('./data/user-agents.txt') as file:
            user_agents = [site.strip() for site in file] #function to turn the txt file content into list
        return user_agents #new list of user_agents in list format

class UserAgent():
    def __init__(self, user_agent):
        self.user_agent = user_agent

    def select_agent(self):
        self.user_agent = random.choice(user_agents)
        return self.user_agent

if __name__ == "__main__":
    user_agents = get_user_agents()
    print (UserAgent.select_agent())

