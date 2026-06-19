/* #include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <algorithm>
using namespace std;


 void dfs(vector<vector<int>>& graph, int v, vector<int>& visited) {
	visited[v] = 1;

	for (int to : graph[v])
		if (!visited[to])
			dfs(graph, to, visited);
} 


int main() {
	int vertexCount, edgeCount;
	cin >> vertexCount >> edgeCount;

	vector<vector<int>> graph(vertexCount);
	for (int i = 0; i < edgeCount; i++) {
		int a, b;
		cin >> a >> b;
		a--;
		b--;

		graph[a].push_back(b);
		graph[b].push_back(a);

	}

		vector<int> visited(vertexCount);
	int componentCount = 0;

	for (int v = 0; v < vertexCount; v++) {
		if (!visited[v]) {
			componentCount++;
			dfs(graph, v, visited);
		}
	}
	
	cout << "Число вершинных связностей: " << componentCount; 


	
	
	return 0;
}*/



#include <iostream>
#include <vector>
#include <fstream>
#include <string>
using namespace std;

void dfs(vector<vector<int>>& graph, int v, vector<int>& visited, int n, int m) {
	visited[v] = 1;
	
	for (int i = 0; i < n; i++) {
		if (graph[v][i] == 1 || graph[v][i] == -1) {
			for (int j = 0; j < m; j++) {
				if ((graph[j][i] == 1 && !visited[j]) || (graph[j][i] == -1 && !visited[j])) {
					dfs(graph, j, visited, n, m);
				}
			}
		}
	}
}


int main() {

	string line;
	cout << "Введите файл: ";
	cin >> line;
	ifstream inputFile(line);
	ofstream outputFile("output.txt");
	int vertexCount, edgeCount;
	inputFile >> vertexCount >> edgeCount;
	
	vector<vector<int>> graph(vertexCount, vector<int>(vertexCount));

	for (int i = 0; i < edgeCount; i++) {
		int a, b;
		inputFile >> a >> b;
			a--;
			b--;
			graph[a][i] = 1;
			graph[b][i] = -1;
	}
	inputFile.close();

	int numConnectedComponents = 0;	
	vector<int> visited(vertexCount, 0);
	
	for (int i = 0; i < vertexCount; i++) {
		if (!visited[i]) {
			dfs(graph, i, visited, edgeCount, vertexCount);
			numConnectedComponents++;
		}
	}

	
	outputFile << "Число компонент связности: " << numConnectedComponents << endl;
	outputFile.close();
	return 0;
}