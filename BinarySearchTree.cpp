#include <iostream>
using namespace std;

struct node {
int value;
node *p_right;
node *p_left;
};

node* insert(node* p_tree, int key);
node* search (node* p_tree, int key);
void destroy(node* p_tree);
node* remove(node* p_tree,int key);

//inserting into the tree
node* insert(node *p_tree,int key)
{
	if (p_tree == NULL)
	{
		node* p_new_tree = new node;
		p_new_tree->p_left = NULL;
		p_new_tree->p_right = NULL;
		p_new_tree->value = key;
		return p_new_tree;
	}
	//Decide to insert into the left subtree
	if (key<p_tree->value)
	{
		p_tree->p_left = insert(p_tree->p_left,key);
	}
	//Insert into the right subtree
	else
	{
		p_tree->p_right = insert(p_tree->p_right,key);
	}
	return p_tree;
}

node* search(node *p_tree,int key)
{
	if (p_tree == NULL)
	{
		return NULL;
	}
	else if (key == p_tree->value)
	{
		return p_tree;
	}
	else if (key<p_tree->value)
	{
		return search(p_tree->p_left,key);
	}
	else
	{
		return search(p_tree->p_right,key);
	}
}

node* find_max(node* p_tree)
{
	if (p_tree == NULL)
	{	
		return NULL;
	}
	if (p_tree->p_right == NULL)
	{
		return p_tree;
	}
	return find_max(p_tree->p_right);
}

node *remove (node *p_tree, int key)
{
	if (p_tree == NULL)
	{
		return NULL;
	}
	if (p_tree->value == key)
	{
		if (p_tree->p_left == NULL)
		{
			node* p_right_sub = p_tree->p_right;
			delete p_tree;
			return p_right_sub;
		}
		if (p_tree->p_right == NULL)
		{
			node* p_left_sub = p_tree->p_left;
			delete p_tree;
			return p_left_sub;
		}
		node* p_max_node = find_max(p_tree->p_left);
		p_max_node->p_left = p_tree->p_left;
		p_max_node->p_right = p_tree->p_right;
		delete p_tree;
		return p_max_node;
	}
	if (key<p_tree->value)
	{
		p_tree->p_left = remove(p_tree->p_left, key);
	}
	if (key>p_tree->value)
	{
		p_tree->p_right = remove(p_tree->p_right, key);
	}
}


int main()
{}