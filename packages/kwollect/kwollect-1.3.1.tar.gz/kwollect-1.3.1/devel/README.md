# Release how-to

- Bump version
```
vim kwollect/__init__.py
vim debian/changelog
git commit -m "v0.1.0"
git tag v0.1.0
```

- (optional) Build .deb package: see `.gitlab-ci.yml`

- Publish
```
git push
git push --tags
```

- Upload on pypy
```
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

# Devel environment with Vagrant

Vagrant box is provisionned with:
- `install.sh`: installs Kwollect and its component from scratch:
  - API (forwarded at localhost:3000)
  - Grafana dashboard (available at <http://localhost:3003/d/kwollect/kwollect-metrics?orgId=1&from=1609451999000&to=1609455599000&var-device_id=Select...&var-metric_id=None>)
- `populate.sh`: populate database with fake data (dated just before January 01, 2021 0:00) and job scheduler integration with job ids 1 and 2

