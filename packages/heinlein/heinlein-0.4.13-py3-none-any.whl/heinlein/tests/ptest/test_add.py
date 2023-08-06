from heinlein import create_project
p = create_project("test2")
a = [1,2,3]
p.check_in("test1.test2",a)
p.check_in("test1.test3.test2", a)



