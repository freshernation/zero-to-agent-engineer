# build_child()     compiled: doubles value
# build_parent()    compiled: adds one to value, then runs the child as a node
# run_parent(value) the final state
#
# run_parent(3) -> value == 8
#
# parent.add_node("child", build_child())
#
# Keep the child's updates to keys the parent is not also writing.
