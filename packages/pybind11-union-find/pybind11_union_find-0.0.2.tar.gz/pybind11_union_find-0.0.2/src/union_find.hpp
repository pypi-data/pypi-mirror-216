#pragma once

#include <vector>
#include <algorithm>
#include <map>
#include <numeric>
#include <string>

struct UnionFind
{
    UnionFind(int n)
    {
        parent = std::vector<int>(n, 0);
        std::iota(parent.begin(), parent.end(), 0);
        rank = std::vector<int>(n, 0);
    }

    int find(int x)
    {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void _union(int x, int y)
    {
        auto px = find(x);
        auto py = find(y);

        if (px == py) {
            return;
        }

        if (rank[px] < rank[py]) {
            std::swap(px, py);
        }

        parent[py] = px;
        if (rank[px] == rank[py]) {
            rank[px] += 1;
        }
    }

    std::vector<std::vector<int>> groups()
    {
        std::map<int, std::vector<int>> group_dict;
        for (int i = 0, n = (int)parent.size(); i < n; ++i) {
            group_dict[find(i)].push_back(i);
        }
        std::vector<std::vector<int>> ret;
        for (auto &pair : group_dict) {
            ret.emplace_back(std::move(pair.second));
        }
        return ret;
    }

    std::vector<int> group_of(int x)
    {
        for (const auto &g : groups()) {
            if (std::find(g.begin(), g.end(), x) != g.end()) {
                return g;
            }
        }
        throw std::invalid_argument("something went wrong, node: " +
                                    std::to_string(x));
    }

    std::vector<int> parent_() const { return parent; }
    std::vector<int> rank_() const { return rank; }

  private:
    std::vector<int> parent;
    std::vector<int> rank;
};
