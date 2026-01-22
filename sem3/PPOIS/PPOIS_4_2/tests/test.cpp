#include "pch.h"
#include "../OrientedGraph.h"

TEST(TestCaseName, TestName) {
  EXPECT_EQ(1, 1);
  EXPECT_TRUE(true);
}

class OrientedGraphTest : public ::testing::Test {
protected:
    OrientedGraph<> graph;

    void SetUp() override {
        graph.Add_Vertex("A");
        graph.Add_Vertex("B");
        graph.Add_Vertex("C");
        graph.Add_Edge("A", "B");
        graph.Add_Edge("A", "A");
        graph.Add_Edge("B", "C");
    }
};

class OrientedGraphTest1 : public OrientedGraph<string> {
public:
    vector<string>& Get_Vertex() {
        return vertex;
    }

    vector<vector<bool>>& Get_AdjacencyMatrix() {
        return adjacency_matrix;
    }
};

TEST_F(OrientedGraphTest, AddVertex) {
    graph.Add_Vertex("D");
    EXPECT_TRUE(graph.Vertex_Exist("D"));
    EXPECT_EQ(graph.Get_Vertex_Amount(), 4);
}

TEST_F(OrientedGraphTest, DeleteVertex) {
    graph.Delete_Vertex("B");
    EXPECT_FALSE(graph.Vertex_Exist("B"));
    EXPECT_EQ(graph.Get_Vertex_Amount(), 2);
    EXPECT_EQ(graph.Get_Edges_Amount(), 1);
}

TEST_F(OrientedGraphTest, AddEdge) {
    graph.Add_Edge("A", "C");
    EXPECT_EQ(graph.Get_Edges_Amount(), 4); 
}

TEST_F(OrientedGraphTest, DeleteEdge) {
    graph.Delete_Edge("A", "B");
    EXPECT_EQ(graph.Get_Edges_Amount(), 2); 
}

TEST_F(OrientedGraphTest, PrintVertices) {
    testing::internal::CaptureStdout();
    graph.Print_Vertices();
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_NE(output.find("A"), std::string::npos);
    EXPECT_NE(output.find("B"), std::string::npos);
    EXPECT_NE(output.find("C"), std::string::npos);
}

TEST_F(OrientedGraphTest, IncidentEdges) {
    testing::internal::CaptureStdout();
    graph.Print_Incident_Edges("A");
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_NE(output.find("(A, B)"), std::string::npos);
    EXPECT_NE(output.find("(A, A)"), std::string::npos); 
}

TEST_F(OrientedGraphTest, AdjacentVertices) {
    testing::internal::CaptureStdout();
    graph.Print_Adjacent_Vertex("A");
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_NE(output.find("B"), std::string::npos);
    EXPECT_NE(output.find("A"), std::string::npos);
}

TEST_F(OrientedGraphTest, AddDuplicateEdge) {
    graph.Add_Edge("A", "B"); 
    EXPECT_EQ(graph.Get_Edges_Amount(), 3); 
}

TEST_F(OrientedGraphTest, DeleteNonExistentEdge) {
    graph.Delete_Edge("B", "A"); 
    EXPECT_EQ(graph.Get_Edges_Amount(), 3); 
}

TEST_F(OrientedGraphTest, AddVertexThatAlreadyExists) {
    graph.Add_Vertex("A"); 
    EXPECT_EQ(graph.Get_Vertex_Amount(), 3); 
}

TEST_F(OrientedGraphTest, VertexDegree) {
    EXPECT_EQ(graph.Vertex_Degree("A"), 2); 
    EXPECT_EQ(graph.Vertex_Degree("B"), 1);
}

TEST_F(OrientedGraphTest, DeleteVertexWithEdges) {
    graph.Delete_Vertex("A"); 
    EXPECT_EQ(graph.Get_Vertex_Amount(), 2); 
    EXPECT_EQ(graph.Get_Edges_Amount(), 1); 
}

TEST_F(OrientedGraphTest, PrintAdjacentVertices) {
    testing::internal::CaptureStdout();
    graph.Print_Adjacent_Vertex("B"); 
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_NE(output.find("A"), std::string::npos);
    EXPECT_NE(output.find("C"), std::string::npos); 
}

TEST_F(OrientedGraphTest, IncidentEdgesWithNonExistentVertex) {
    testing::internal::CaptureStdout();
    graph.Print_Incident_Edges("D"); 
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(output.find("Incident Edges: "), 0); 
}

TEST_F(OrientedGraphTest, EdgeExistenceCheck) {
    testing::internal::CaptureStdout();
    graph.Edge_Exist("A", "B"); 
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_NE(output.find("Edge already exists"), std::string::npos); 
}

TEST_F(OrientedGraphTest, VertexExistenceCheck) {
    EXPECT_TRUE(graph.Vertex_Exist("C")); 
    EXPECT_FALSE(graph.Vertex_Exist("D")); 
}

TEST_F(OrientedGraphTest, ClearGraph) {
    graph.clear(); 
    EXPECT_TRUE(graph.empty()); 
    EXPECT_EQ(graph.Get_Vertex_Amount(), 0); 
    EXPECT_EQ(graph.Get_Edges_Amount(), 0); 
}

TEST_F(OrientedGraphTest, EmptyGraph) {
    EXPECT_FALSE(graph.empty()); 
    graph.clear();
    EXPECT_TRUE(graph.empty()); 
}

TEST_F(OrientedGraphTest, EdgeIteratorFunctionality) {
    EdgeIterator<string> it = graph.edges_begin();
    EXPECT_EQ(*it, make_pair("A", "B")); 

    ++it;
    EXPECT_EQ(*it, make_pair("A", "A")); 

    ++it; 
    EXPECT_EQ(*it, make_pair("B", "C")); 

    ++it; 
    EXPECT_EQ(*it, make_pair("B", "C"));
    EXPECT_EQ(it.Get_Index(), 3); 
}

TEST_F(OrientedGraphTest, IncidentEdgeIteratorFunctionality) {
    IncidentEdgeIterator<string> it = graph.incident_edges_begin("A");
    EXPECT_EQ(*it, make_pair("A", "B")); 

    ++it; 
    EXPECT_EQ(*it, make_pair("A", "A")); 

    ++it; 
    EXPECT_EQ(it != graph.incident_edges_end("A"), false); 
}

TEST_F(OrientedGraphTest, AdjacentVertexIteratorFunctionality) {
    OrientedGraphTest1 graph1;
    graph1.Add_Vertex("A");
    graph1.Add_Vertex("B");
    graph1.Add_Vertex("C");
    graph1.Add_Edge("A", "B");
    graph1.Add_Edge("B", "C");
    AdjacentVertexIterator<string> it(graph1.Get_Vertex(), graph1.Get_AdjacencyMatrix(), "A", 0);
    EXPECT_EQ(*it, "B"); 
    ++it;
    EXPECT_EQ(it != AdjacentVertexIterator<string>(graph1.Get_Vertex(), graph1.Get_AdjacencyMatrix(), "A", -1), false);
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}