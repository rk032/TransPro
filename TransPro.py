import tkinter as tk
from tkinter import messagebox, scrolledtext

class TransportationProblemSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Transportation Problem Solver")

        self.create_input_widgets()
        self.create_result_widgets()

    def create_input_widgets(self):
        input_frame = tk.Frame(self.root, padx=20, pady=20)
        input_frame.grid(row=0, column=0, padx=10, pady=15, sticky="n")
    
        tk.Label(input_frame, text="Transport Problem:", font=("Helvetica", 14)).grid(row=0, column=0, pady=10, sticky="w")
    
        tk.Label(input_frame, text="Number of Sources:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=15, sticky="w")
        self.row_entry = tk.Entry(input_frame, font=("Helvetica", 12))
        self.row_entry.grid(row=1, column=1, padx=5, pady=5)
    
        tk.Label(input_frame, text="Number of Destinations:", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=15, sticky="w")
        self.column_entry = tk.Entry(input_frame, font=("Helvetica", 12))
        self.column_entry.grid(row=2, column=1, padx=5, pady=5)
    
        tk.Label(input_frame, text="Supplies (comma-separated):", font=("Helvetica", 12)).grid(row=3, column=0, padx=5, pady=15, sticky="w")
        self.supplies_entry = tk.Entry(input_frame, font=("Helvetica", 12))
        self.supplies_entry.grid(row=3, column=1, padx=5, pady=5)
    
        tk.Label(input_frame, text="Demands (comma-separated):", font=("Helvetica", 12)).grid(row=4, column=0, padx=5, pady=15, sticky="w")
        self.demands_entry = tk.Entry(input_frame, font=("Helvetica", 12))
        self.demands_entry.grid(row=4, column=1, padx=5, pady=5)
    
        tk.Label(input_frame, text="Costs (comma-separated, row-wise):", font=("Helvetica", 12)).grid(row=5, column=0, padx=5, pady=15, sticky="w")
        self.costs_entry = tk.Entry(input_frame, font=("Helvetica", 12))
        self.costs_entry.grid(row=5, column=1, padx=5, pady=5)
    
        self.solve_button = tk.Button(input_frame, text="Solve", command=self.solve_problem, font=("Helvetica", 12))
        self.solve_button.grid(row=6, column=0, columnspan=2, pady=10, sticky="n")
    
    def create_result_widgets(self):
        result_frame = tk.Frame(self.root, padx=20, pady=20)
        result_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
    
        tk.Label(result_frame, text="Results:", font=("Helvetica", 14)).grid(row=0, column=0, pady=10, sticky="w")
    
        self.result_text = scrolledtext.ScrolledText(result_frame, width=40, height=13, wrap=tk.WORD, font=("Helvetica", 12))
        self.result_text.grid(row=1, column=0, pady=15, padx=5)

    def solve_problem(self):
        try:
            num_sources = int(self.row_entry.get())
            num_destinations = int(self.column_entry.get())

            supplies = list(map(int, self.supplies_entry.get().split(',')))
            demands = list(map(int, self.demands_entry.get().split(',')))
            costs = list(map(int, self.costs_entry.get().split(',')))

            if len(supplies) != num_sources or len(demands) != num_destinations or len(costs) != num_sources * num_destinations:
                raise ValueError("Invalid input dimensions.")

            result_nw, cost_nw = self.north_west(num_sources, num_destinations, supplies.copy(), demands.copy(), costs.copy())
            result_lc, cost_lc = self.least_cost(num_sources, num_destinations, supplies.copy(), demands.copy(), costs.copy())
    
            result_str = (
                self.format_matrix(result_nw, cost_nw, "Northwest Corner")
                + self.format_matrix(result_lc, cost_lc, "Least Cost")
            )
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_str)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def north_west(self, num_sources, num_destinations, supplies, demands, costs):
        allocations = [[0] * num_destinations for _ in range(num_sources)]
        total_cost = 0

        i, j = 0, 0

        while i < num_sources and j < num_destinations:
            quantity = min(supplies[i], demands[j])
            allocations[i][j] = quantity

            total_cost += quantity * costs[i * num_destinations + j]

            supplies[i] -= quantity
            demands[j] -= quantity

            if supplies[i] == 0:
                i += 1
            if demands[j] == 0:
                j += 1

        return allocations, total_cost

    def least_cost(self, num_sources, num_destinations, supplies, demands, costs):
        allocations = [[0] * num_destinations for _ in range(num_sources)]
        total_cost = 0

        while True:
            min_cost = float('inf')
            min_i, min_j = -1, -1

            for i in range(num_sources):
                for j in range(num_destinations):
                    if supplies[i] > 0 and demands[j] > 0 and costs[i * num_destinations + j] < min_cost:
                        min_cost = costs[i * num_destinations + j]
                        min_i, min_j = i, j

            if min_i == -1 or min_j == -1:
                break

            quantity = min(supplies[min_i], demands[min_j])
            allocations[min_i][min_j] = quantity

            total_cost += quantity * min_cost

            supplies[min_i] -= quantity
            demands[min_j] -= quantity

        return allocations, total_cost

    def format_matrix(self, matrix, total_cost, method_name):
        header = f"\n{method_name} Method:\n{'-' * 30}\n"
    
        matrix_str = "\n".join(["\t".join(map(str, row)) for row in matrix])
        matrix_output = f"{header}{matrix_str}\n"
    
        total_cost_output = f"\nTotal Cost for {method_name} Method: {total_cost}\n"
    
        return f"{matrix_output}{total_cost_output}\n"



if __name__ == "__main__":
    root = tk.Tk()
    app = TransportationProblemSolver(root)
    root.mainloop()
