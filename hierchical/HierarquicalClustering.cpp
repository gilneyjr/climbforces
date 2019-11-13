#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <cmath> // sqrt

#include <forward_list>
#include <map>
#include <iterator>

// test 2
#include <set>
#include <algorithm> // copy

using namespace std;

// New:

// swap elements:
// clusters[1].swap(clusters[4]);

template <typename Data_t, typename Dist_t>
class HierarquicalClustering
{
public:
    struct Cluster {
        size_t id;
        bool isLeaf;
        union {
            struct {
                Cluster* c1;
                Cluster* c2;
            } children;
            Data_t *data;
        } content;

        Cluster(size_t id, Cluster* c1, Cluster* c2) {
            this->id = id;
            this->isLeaf = false;
            this->content.children.c1 = c1;
            this->content.children.c2 = c2;
        }

        Cluster(size_t id, Data_t* data) {
            this->id = id;
            this->isLeaf = true;
            this->content.data = data;
        }
    };

private:
    struct Comparator {
        bool operator()(const Cluster* a, const Cluster *b) { return a->id < b->id; }
    };

    set<Cluster*, Comparator> clusters;
    forward_list<Data_t> data; 

public:
    HierarquicalClustering() {}
    ~HierarquicalClustering() {}

    Dist_t dist(forward_list<Data_t*> &a, forward_list<Data_t*> &b) {
        return 10;
    }

    // TODO:
    Dist_t dist(Cluster *a, Cluster *b) {
        if(a->isLeaf){
            if(b->isLeaf) {
                Data_t &data_a = *(a->content.data);
                Data_t &data_b = *(b->content.data);
                return data_a.dist(data_b);
            }
            else
                return min(dist(a, b->content.children.c1), dist(a, b->content.children.c2));
        } 
        else
            return min(dist(a->content.children.c1,b), dist(a->content.children.c2,b));
    }

    void setData(forward_list<Data_t> &data) {
        this->data = data;
    }

    // vector<vector<Data_t>> getClustering(size_t n) {
    //     if(n == 0)
    //         return forward_list<forward_list<Data_t>>();

    //     vector<vector<Data_t>> vec;

    // } 

    // TODO: Remove after
    void print(Cluster* c, size_t ident = 0, bool first = true) {
        if(!first) {
            for(size_t i = 0; i < ident; ++i)
                cout << ' ';
            cout << "+> ";
        }

        if(c->isLeaf)
            cout << "C" << c->id << " -> " << *(c->content.data) << endl;
        else {
            cout << "C" << c->id << " -> ";
            print(c->content.children.c1, ident+6, true);
            print(c->content.children.c2, ident+3+(first ? 0 : 3), false);
        }
    }

    void run2() {
        if(not clusters.empty()) return;
        if(data.empty()) return;

        // Put each data in a singleton cluster
        for(auto &e : data) {
            clusters.insert(new Cluster(clusters.size(), &e));
        }

        size_t newid = clusters.size();

        while(clusters.size() > 1) {
            auto c1 = clusters.begin();
            auto c2 = ++clusters.begin();
            Dist_t d = dist(*c1, *c2);

            for(auto it1 = c1; it1 != clusters.end(); it1++)
                for(auto it2 = next(it1); it2 != clusters.end(); it2++) {
                    Dist_t new_d = dist(*it1, *it2);
                    if(new_d < d) {
                        d = new_d;
                        c1 = it1;
                        c2 = it2;
                    }
                }

            // Merge
            cout << "C" << (*c1)->id << endl;
            cout << "C" << (*c2)->id << endl;
            cout << "{ ";
            for(auto &c : clusters) 
                cout << "C" << c->id << ' ';
            cout << "}\n";
            
            clusters.insert(new Cluster(newid++, *c1, *c2));
            clusters.erase(c1);
            clusters.erase(c2);

            cout << "{ ";
            for(auto &c : clusters) 
                cout << "C" << c->id << ' ';
            cout << "}\n\n";
        }

        Cluster* c = *(clusters.begin());
        print(c);
    }

    void run(forward_list<Data_t> data) {
        map< size_t, forward_list<Data_t*> > clusters;

        // Put each data in a singleton cluster
        size_t i = 0;
        for(auto &e : data)
            clusters[i++] = {&e};

        while(clusters.size() > 1) {
            auto c1 = clusters.begin();
            auto c2 = ++clusters.begin();
            Dist_t d = dist(c1->second, c2->second);

            for(auto it1 = c2; it1 != clusters.end(); it1++)
                for(auto it2 = next(it1); it2 != clusters.end(); it2++) {
                    Dist_t new_d = dist(it1->second, it2->second);
                    if(new_d < d) {
                        d = new_d;
                        c1 = it1;
                        c2 = it2;
                    }
                }
            //merge(c1->second,c2->second);
        }
    }
};


class Data {
private:
    float x;
    float y;

public:
    Data(float x, float y) : x(x), y(y) {}
    Data(const Data &data) {
        this->x = data.x;
        this->y = data.y;
    }

    double dist(Data &d) {
        return sqrt((d.x-x)*(d.x-x)+(d.y*y)*(d.y*y));
    }

    friend ostream& operator<<(ostream& out, Data& d) {
        out << '(' << d.x << ',' << d.y << ')';
        return out;
    }
};

// template <typename dist_t, class Data_t>
// class Cluster {
// private:
//  Data_t *data;
//  Cluster *c1;
//  Cluster *c2;
//  Cluster *next;

// public:
//  Cluster(Data_t &data) {
//      this->data = new Data_t(data);
//      this->c1 = nullptr;
//      this->c2 = nullptr;
//  }

//  dist_t dist(Cluster &c) {
        
//  }

//  static void merge(Cluster &c1, Cluster &c2) {
        
//  }

//  static Cluster* void group(container<Data_t> dataset) {
//      container<Cluster> clusters;
//      for(auto &e : dataset)
//          clusters.emplace(e);

//      while(clusters.size() > 1) {
//          auto c1 = clusters.begin();
//          auto c2 = clusters.begin()++;
//          dist_t d = c1->dist(*c2);

//          for(auto it1 = c2+1; it1 != clusters.end(); it1++) {
//              for(auto it2 = it1+1; it2 < clusters.end(); it2++) {
//                  dist_t d1 = it1->dist(*it2);
//                  if(d1 < d) {
//                      d = d1;
//                      c1 = it1;
//                      c2 = it2;
//                  }
//              }
//          }

//          merge(c1, c2);
//      }
//  }
// };

void generate(forward_list<Data> &list, size_t n = 5) {
    // Configure random generator
    unsigned seed = 10689; //chrono::system_clock::now().time_since_epoch().count();
    default_random_engine generator(seed);
    uniform_real_distribution<float> distribution(-100, 100);
    
    // Generate n random numbers and add to list
    cout << "Generated data:\n";
    for (int i = 0; i < 5; ++i) {
        float rndX = distribution(generator);
        float rndY = distribution(generator);
        cout << '(' << rndX << ',' << rndY << ')' << endl;
        list.emplace_front(rndX,rndY);
    }
    cout << endl;
}

int main() {
    forward_list<Data> list = forward_list<Data>();
    generate(list);


    auto hc = HierarquicalClustering<Data, double>();
    hc.setData(list);
    hc.run2();

    // vector<Cluster> c;

    // // Put each element in a cluster
    // for(auto & e: v)
    //  c.push_back({.c1=nullptr, .c2=nullptr, .data=e});

    // while(v.size() > 1) {
    //  auto min_c1 = v.begin();    
    //  auto min_c2 = ++(v.begin());

    //  float _dist = dist(*min_c1, *min_c2);
    //  for(auto it1 = v.begin(); it1 != v.end(); it1++) {
    //      for(auto it2 = it1+1; it2 != end(); it2++) {
    //          float tmp = dist(*it1, *it2);
    //          if(tmp <= _dist) {
    //              _dist = tmp;
    //              min_c1 = it1;
    //              min_c2 = it2;
    //          }
    //      }
    //  }

        
    // }
    return 0;
}