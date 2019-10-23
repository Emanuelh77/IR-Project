import re
import collections

def process_file(filepath):
    global current_session
    global session_Id
    global queryDict
    global sessionDict
    global queryFreq
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            try:
                line = line.rstrip('\n')
                tokens = line.split("\t")
                session = int(tokens[0])
                
                if session != current_session:
                    current_session = session
                    session_Id = session_Id + 1;
                query = tokens[1]
                timestamp = tokens[2]
                if query in queryDict.keys():
                    queryDict[query].append(session_Id)
                else:
                    queryDict.update({query : [session_Id]})
                if session_Id in sessionDict.keys():
                    sessionDict[session_Id].append(query)
                else:
                    sessionDict.update({session_Id : [query]})
                if query in queryFreq.keys():
                    queryFreq[query] += 1
                else:
                    queryFreq.update({query : 1})
            except ValueError:
                print("bad row")
        
        
def find_candidate_queries(query, qLength):
    query = query.lower()
  #print(query)
  #print(qLength)
    if query in queryDict.keys():
        sessionsList = queryDict[query]
        
        cq = {}
        for session in sessionsList:
          #print(sessionDict[session])
            if session in sessionDict.keys():
                for s in sessionDict[session]:
                    if s.startswith(query) and len(re.findall(r'\w+', s)) > qLength:
                        if s in cq.keys():
                            cq[s] += 1
                        else:
                            cq.update({s : 1})

        ranked_candidates = {}
        for q in cq.items():
            cqScore = score(query, q[0], q[1])
            ranked_candidates.update({q[0] : cqScore})

        sorted_candidates = sorted(ranked_candidates.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_candidates
      
    else:
        return "Query not in log"
  
  
def score(query, cq, cqFreq):
    global maxQueryFreq
    freq = cqFreq/maxQueryFreq
    sessionsWithQuery = queryDict[query]
    sessionsWithCq = queryDict[cq]
    queryToCq = len(set(sessionsWithQuery) & set(sessionsWithCq))
    mod = queryToCq/len(sessionsWithQuery)
  
    return (freq + mod)/(1 - min(freq,mod))
  


# In[3]:


current_session = 0
session_Id = 0
queryDict = {}
sessionDict = {}
queryFreq = {}

process_file(r'Clean-Data-01.txt')
process_file(r'Clean-Data-02.txt')
process_file(r'Clean-Data-03.txt')
process_file(r'Clean-Data-04.txt')
process_file(r'Clean-Data-05.txt')

maxQueryFreq = max(queryFreq.values())


# In[26]:


def suggest(q):
    qLen = len(re.findall(r'\w+', q))
    can_q = find_candidate_queries(q,qLen)
    if len(can_q) < 3:
        return [x[0] for x in can_q]
    else:
        return [x[0] for x in can_q[0:3]]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




