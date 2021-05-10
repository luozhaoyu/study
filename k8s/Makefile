recreate:
	kubectl delete -f k8s_example.yaml
	kubectl create -f k8s_example.yaml
	sleep 2;
	kubectl get pods

apply:
	kubectl apply -f k8s_example.yaml

debug:
	kubectl debug -it zhaoyu-example-postgresql-0 --image=busybox --target=zhaoyu-example-postgresql-0

port-forward:
	kubectl port-forward service/zhaoyu-example-postgresql 4444:4444
