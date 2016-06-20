def h_vector():
	h_vecs=open("h_vectors_hypersimplices_3_dual",'w')
	with open("f_vectors_hypersimplices_3",'r') as f_vecs:
		for i in xrange(12):				
			h_vecs.write(f_vecs.readline())
			f_vecs.readline()
			h_vecs.write("H_VECTOR\n")
			top_row=[1]+[int(x) for x in f_vecs.readline().strip().split(" ")][::-1]
			f_vecs.readline()
			matrix=[[0 for x in xrange(len(top_row))] for x in xrange(len(top_row))]
			matrix[0]=top_row
			for i in xrange(len(top_row)):
				matrix[i][0]=1
			for j in xrange(1,len(top_row)):
				for i in xrange(1,len(top_row)):
					matrix[j][i]=matrix[j-1][i]-matrix[j][	i-1]
			h_vector = [matrix[1+x][len(top_row)-1-x] for x in xrange(len(top_row)-1)][::-1]
			h_vecs.write("1 ")
			for h_i in h_vector:
				h_vecs.write(str(h_i)+" ")
			h_vecs.write('\n\n')
h_vector()
