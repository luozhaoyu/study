https://kubernetes.io/docs/
https://github.com/kubernetes/
https://kubernetes.io/blog/

https://kubernetes.io/docs/reference/kubectl/cheatsheet/
https://www.reddit.com/r/kubernetes/comments/gldbkk/cka_exam_good_exercisemock_exam_resources/


https://killer.sh/course/preview/e84d0e31-4fff-4c42-8afd-be1bdbc0d994
ETCD
https://medium.com/techlog/whats-inside-etcd-a-deep-dive-into-the-kubernetes-world-84a677754c31


```
ETCDCTL_API=3 etcdctl --endpoints $ADVERTISE_URL --cacert /var/lib/minikube/certs/etcd/ca.crt  --cert /var/lib/minikube/certs/etcd/server.crt --key /var/lib/minikube/certs/etcd/server.key snapshot status abc
```