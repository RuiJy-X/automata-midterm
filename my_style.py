class DFA():
    def __init__(self):
        self.states = set()
        self.start = None
        self.accepts = set()
        self.alphabets = set()
        self.transitions = {}
        
    def add_state(self, name,is_start = False, is_accept= False):
        self.states.add(name)
        
        if is_start:
            self.start = name
        if is_accept:
            self.accepts.add(name)
        if name not in self.transitions:
            self.transitions[name] = {}
        return name
    
    def add_transition(self,from_state,symbol, to_state):
        self.alphabets.add(symbol)
        self.transitions[from_state][symbol] = to_state
    
    def get_next_state(self,state,symbol):
        try:
            return self.transitions[state][symbol]
            
        except KeyError:
            return None
        
    def myhill_nerode(self):
        distinction_table = {}
        n = len(self.states)
        states = sorted(list(self.states))
        
        for i in range(n):
            for j in range(i+1,n):
                p = states[i]
                q = states[j]
                
                if (p in self.accepts) != (q in self.accepts):
                    distinction_table[(p,q)] = True
                else:
                    distinction_table[(p,q)] = False
                
        change = True
        while change:
            change = False
            
            for i in range(n):
                for j in range(i+1,n):
                    p = states[i]
                    q = states[j]
                    
                    if not distinction_table[(p,q)]:
                        for sym in self.alphabets:
                            p_next = self.get_next_state(p,sym)
                            q_next = self.get_next_state(q,sym)
                            
                            
                            if p_next and q_next:
                                s1,s2 = sorted((p_next,q_next))
                                if s1 != s2 and distinction_table.get((s1,s2),False):
                                    distinction_table[(p,q)] = True
                                    change = True
                                    break
        return distinction_table
            

        
        
    def display(self):
        print("NFA Transition Table:")
    
        # collect all symbols across transitions
        symbols = sorted({sym for trans in self.transitions.values() for sym in trans})
        
        # header row
        header = "State\t" + "\t".join(symbols)
        print(header)
        
        # each state row
        for state in sorted(self.states):   # sort for consistent order
            row = [state]
            for sym in symbols:
                dests = self.transitions[state].get(sym, None)
                if dests:
                    row.append("".join(dests))  # show multiple destinations
                else:
                    row.append("Φ")
            print("\t".join(row))
            
    def create_table(self, table):
        states = sorted(self.states)
        n = len(states)
        print(f"\t{"\t".join(states[::-1])}")
        for i in range(n):
            row = []
            for j in range(n-1,i,-1):
                p = states[i]
                q = states[j]
                
                
                if table.get((p,q), True):
                    row.append("X")
                else:
                    row.append("/")
                
            print(f"{states[i]}\t{"\t".join(row)}")
        
            
def main():
    dfa = DFA()
    dfa.add_state("q0", is_start=True)
    dfa.add_state("q1")
    dfa.add_state("q2")
    dfa.add_state("q3", is_accept=True)
    
    dfa.add_transition("q0", "a", "q3")
    dfa.add_transition("q1", "a", "q3")
    dfa.add_transition("q0", "b", "q2")
    dfa.add_transition("q1", "b", "q2")
    
    dfa.add_transition("q2", "a", "q0")
    dfa.add_transition("q2", "b", "q1")
    
    # Add trap/self loop for q3 to make it complete DFA for 'a' and 'b'
    dfa.add_transition("q3", "a", "q3")
    dfa.add_transition("q3", "b", "q3")

    

    dfa.display()
    
    table = dfa.myhill_nerode()

    print("\n--- Myhill-Nerode Table ---")    
    dfa.create_table(table)
    
    print("\n--- Distinguishability Table (True=Distinct, False=Equivalent) ---")
    for pair, is_distinct in table.items():
        relation = "Distinct" if is_distinct else "EQUIVALENT"
        print(f"Pair {pair}: {relation}")
    

if __name__ == "__main__":
    main()
