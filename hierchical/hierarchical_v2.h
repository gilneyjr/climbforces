#ifndef HIERARCHICAL
#define HIERARCHICAL
#include <vector>

using std::vector;

template <typename Data>
class Dendogram {
private:
	// Data structures declarations
	class AbstractNode {};

	class Leaf : public AbstractNode {
	public:
		Data *data;
	};

	class Cluster : public AbstractNode {
	public:
		Cluster *left;
		Cluster *right;
	};

	// Attributes
	AbstractNode *head;

public:
	Dendogram();
	~Dendogram();

	void group(vector<Data> dataset);
};

#endif