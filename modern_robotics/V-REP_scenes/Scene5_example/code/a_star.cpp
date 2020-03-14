#include <iostream>
#include <string> 
#include <fstream>
#include <sstream>
#include <stdlib.h>
#include <limits> // for infinity
#include <vector>
#include <algorithm>

using namespace std; 

#define NUM_OF_NODE 12
#define GOAL 12
#define START 1

class node { 
public: 
    //Updatable variable
    int parenet_node; // parent of this node (ID)
    double past_cost;
    
    //Intrinstic information 
    vector<int>    edge_list; // [neighbor_id_1 ,neighbor_id_2, neighbor_id_3, ....]
    vector<double> edge_cost; // [edge_cost_1   ,edge_cost_2,   edge_cost_3, ...]
    double heuristic_cost;
    
    // class constructor
    node(double heu_cost): heuristic_cost(heu_cost), past_cost(numeric_limits<double>::infinity()), parenet_node(-1){}
};

int pop_min(vector<int>& open_list,vector<node>& node_list)
/*
return node-id, with minimum cost in open_list
If open_list is empty, return -1
*/
{
    int id = -1 ;
    double min_value = numeric_limits<double>::infinity();
    for (int i = 0 ; i < open_list.size(); i++)
    {
        double total_cost = node_list.at(open_list.at(i)).heuristic_cost + node_list.at(open_list.at(i)).past_cost;
        if (total_cost < min_value)
        {
            //Update min value and id
            min_value = total_cost;
            id = open_list.at(i);
        }
    }
    if (id == -1) return id ;//open_list is empty

    // pop out id from open_list and return id 
    open_list.erase(remove(open_list.begin(), open_list.end(), id), open_list.end());
    return id;
}

int main()
{
    /********************************************************
    ******** Get inform from nodes.csv and edges.csv ********
    *********************************************************/
    //Init node list, ID is indice of list
    vector<node> node_list; // start from 1 not 0.
    node_list.assign(NUM_OF_NODE+1,0);// init node_list
    //readfile
    fstream file;
    file.open("../result/nodes.csv");
    string line;
    while (getline(file, line,'\n'))  // Read line until meat '\n'
    {
        if (line[0] == '#')continue; // ignore comment line 
	    istringstream templine(line); // string convert to stream
	    string data;
        vector<double> tmp_float_data;
	    while (getline( templine, data,',')) //Read line until meat ','
	    {
            tmp_float_data.push_back(atof(data.c_str()));  //string convert to float
	    }
        node n(tmp_float_data[3]);
        node_list.at(int(tmp_float_data[0])) = n;
	}
    file.close();

    file.open("../result/edges.csv");
    while (getline(file, line,'\n'))  // Read line until meat '\n'
    {
        if (line[0] == '#')continue; // ignore comment line 
	    istringstream templine(line); // string convert to stream
	    string data;
        vector<double> tmp_float_data;
	    while (getline( templine, data,',')) //Read line until meat ','
	    {
            tmp_float_data.push_back(atof(data.c_str()));  //string convert to float
	    }
        // put edge cost into both node's edge_list
        node_list.at(int(tmp_float_data[0])).edge_list.push_back( int(tmp_float_data[1]) );
        node_list.at(int(tmp_float_data[0])).edge_cost.push_back(     tmp_float_data[2]  );

        node_list.at(int(tmp_float_data[1])).edge_list.push_back( int(tmp_float_data[0]) );
        node_list.at(int(tmp_float_data[1])).edge_cost.push_back(     tmp_float_data[2]  );
	}
    file.close();
    
    /****************************
    ******** A* Planning ********
    ****************************/
    vector<int> open_list; // node-ID
    vector<int> close_list; // node-ID

    // init start point
    open_list.push_back(START); 
    node_list.at(START).past_cost = 0;
    node_list.at(START).parenet_node = 1;

    while (not open_list.empty())
    {
        int current = pop_min(open_list,node_list);
        close_list.push_back(current);
        // Check if already reached goal
        if (current == GOAL)break;

        // iterate its edge list(neiborhor), ignore node in closelist, update past cost and add to open list 
        for ( int i = 0 ; i < node_list.at(current).edge_list.size(); i++)
        {
            int    neighbor      = node_list.at(current).edge_list.at(i);
            double neighbor_cost = node_list.at(current).edge_cost.at(i);
            
            //if neighbor is already in closelist -> skip it.
            vector<int>::iterator it = find(close_list.begin(), close_list.end(), neighbor);
            if (it != close_list.end())continue;
            
            //calculate new_cost
            double tentative_past_cost = node_list.at(current).past_cost + neighbor_cost;

            // If new cost is smaller, then update past_cost and parenet node
            if (tentative_past_cost < node_list.at(neighbor).past_cost)
            {
                node_list.at(neighbor).past_cost    = tentative_past_cost;
                node_list.at(neighbor).parenet_node = current;
                //Put it into open_list
                open_list.push_back(neighbor);
            }
        }
    }
    cout << "reached goal" << endl;
    /***********************************
    ********  traverse A* path  ********
    ***********************************/
    // recursive traverse A* path
    int x = GOAL;
    vector<int> inv_path; // inverse path,start from GOAL, end at START
    inv_path.push_back(x);
    while (x != START)
    {
        x = node_list.at(x).parenet_node;
        inv_path.push_back(x);
    }

    for (vector<int>::iterator it = inv_path.begin() ; it != inv_path.end(); it++)cout << *it << endl;
        
    /*************************************
    ********  Output to path.csv  ********
    *************************************/
    ofstream output_file ("../result/path.csv");
    while (!inv_path.empty())
    {
        output_file << inv_path.back();//reverse-order
        inv_path.pop_back();
        if (!inv_path.empty()) output_file << ",";
    }
    output_file.close();
    return 0;
}
