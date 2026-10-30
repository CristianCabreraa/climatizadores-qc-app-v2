#!/usr/bin/env python3
"""Aplica las mejoras GreenAir V2 a una copia del repositorio original.
Ejecutar desde el directorio del proyecto: python aplicar_correcciones.py .
No elimina ficheros ajenos; crea copias de seguridad en __backup_greenair_v2.
"""
from pathlib import Path
import sys,re,shutil,json,datetime,base64
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
kit=Path(__file__).resolve().parent
modified={}
EMBEDDED_OVERRIDES = {'js/share.js': 'LyoqIEd1YXJkYWRvIHkgY29tcGFydGljacOzbiBkZSBhcmNoaXZvcyByZWFsZXM6IEFuZHJvaWQgbmF0aXZvIC8gV2ViIFNoYXJlIC8gbmF2ZWdhZG9yLiAqLwpjb25zdCB0b0Jhc2U2NCA9IChibG9iKSA9PiBuZXcgUHJvbWlzZSgocmVzb2x2ZSwgcmVqZWN0KSA9PiB7CiAgY29uc3QgcmVhZGVyID0gbmV3IEZpbGVSZWFkZXIoKTsKICByZWFkZXIub25lcnJvciA9ICgpID0+IHJlamVjdChuZXcgRXJyb3IoJ05vIHNlIHB1ZG8gbGVlciBlbCBQREYnKSk7CiAgcmVhZGVyLm9ubG9hZCA9ICgpID0+IHJlc29sdmUoU3RyaW5nKHJlYWRlci5yZXN1bHQpLnNwbGl0KCcsJylbMV0pOwogIHJlYWRlci5yZWFkQXNEYXRhVVJMKGJsb2IpOwp9KTsKCmV4cG9ydCBjb25zdCBTaGFyZUVuZ2luZSA9IHsKICBidWlsZFN1bW1hcnkobWV0YSA9IHt9LCBmaWxlTmFtZSA9ICcnKSB7CiAgICBjb25zdCBjcCA9IG1ldGEuY2hlY2twb2ludHMgfHwge307CiAgICBjb25zdCByZXN1bHRzID0gWwogICAgICBbJ1ByZXNvc3RhdG9zJywgY3AucHJlc29zdGF0b3NdLAogICAgICBbJ1ZlbnRpbGFkb3IgZGUgaW1wdWxzacOzbicsIGNwLnZlbnRJbXB1bHNpb25dLAogICAgICBbJ1ZlbnRpbGFkb3IgZGUgcmV0b3JubycsIGNwLnZlbnRSZXRvcm5vXSwKICAgICAgWydUZW1wZXJhdHVyYSBkZSBpbXB1bHNpw7NuJywgY3AudGVtcEltcHVsc2lvbl0sCiAgICAgIFsnVGVtcGVyYXR1cmEgZGUgcmV0b3JubycsIGNwLnRlbXBSZXRvcm5vXQogICAgXS5tYXAoKFtuYW1lLCBva10pID0+IGAke25hbWV9OiAke29rID8gJ0NPUlJFQ1RPJyA6ICdJTkNPUlJFQ1RPJ31gKS5qb2luKCdcbicpOwogICAgcmV0dXJuIGAqR1JFRU5BSVIgSU5EVVNUUklBTCDigJQgRklDSEEgREUgQ09OVFJPTCBZIFBSVUVCQVMqXG5gICsKICAgICAgYCpOwrogUGVkaWRvOiogJHttZXRhLm9yZGVyTnVtYmVyIHx8ICdTSU4gUEVESURPJ31cbmAgKwogICAgICBgKk7CuiBTZXJpZToqICR7bWV0YS5zZXJpYWxOdW1iZXIgfHwgJ04vQSd9XG5gICsKICAgICAgYCpNb2RlbG86KiAke21ldGEubW9kZWwgfHwgJ04vQSd9XG5gICsKICAgICAgYCpDdWFkcm86KiAke21ldGEuY3VhZHJvIHx8ICdOL0EnfVxuYCArCiAgICAgIGAqQ29uZmlndXJhY2nDs246KiAke21ldGEuY29uZmlndXJhY2lvbiB8fCAnTi9BJ31cbmAgKwogICAgICBgKlNvbmRhIENPMjoqICR7bWV0YS5vcHRpb25hbHM/LnNvbmRhQ28yPy5oYXMgPyAobWV0YS5vcHRpb25hbHMuc29uZGFDbzIudHlwZSB8fCAnTm8gZXNwZWNpZmljYWRhJykgOiAnTm8gaW5zdGFsYWRhJ31cbmAgKwogICAgICBgKk1vbnRhZG9yOiogJHttZXRhLnBlcnNvbm5lbD8ubW9udGFkb3IgfHwgJ04vQSd9XG5gICsKICAgICAgYCpFbGVjdHJpY2lzdGE6KiAke21ldGEucGVyc29ubmVsPy5lbGVjdHJpY2lzdGEgfHwgJ04vQSd9XG5gICsKICAgICAgYCpWZXJpZmljYWNpb25lczoqXG4ke3Jlc3VsdHN9XG5gICsKICAgICAgYCpQREY6KiAke2ZpbGVOYW1lfVxuYCArCiAgICAgIGBGZWNoYTogJHtuZXcgRGF0ZSgpLnRvTG9jYWxlU3RyaW5nKCdlcy1FUycpfWA7CiAgfSwKCiAgYXN5bmMgc2F2ZVBkZihibG9iLCBmaWxlTmFtZSkgewogICAgaWYgKCEoYmxvYiBpbnN0YW5jZW9mIEJsb2IpIHx8ICFibG9iLnNpemUpIHJldHVybiB7IHN1Y2Nlc3M6IGZhbHNlLCBtZXNzYWdlOiAnUERGIHZhY8OtbyBvIG5vIHbDoWxpZG8uJyB9OwogICAgaWYgKHdpbmRvdy5HcmVlbkFpck5hdGl2ZT8uc2F2ZVBkZikgewogICAgICB0cnkgewogICAgICAgIC8vIEVsIMOpeGl0byByZWFsIHNlIHJlY2liZSBkZXNwdcOpcyBkZSBxdWUgQW5kcm9pZCBlc2NyaWJhIGVsIGFyY2hpdm8uCiAgICAgICAgd2luZG93LkdyZWVuQWlyTmF0aXZlLnNhdmVQZGYoYXdhaXQgdG9CYXNlNjQoYmxvYiksIGZpbGVOYW1lKTsKICAgICAgICByZXR1cm4geyBzdWNjZXNzOiBmYWxzZSwgcGVuZGluZzogdHJ1ZSwgbWV0aG9kOiAnYW5kcm9pZF9waWNrZXInLCBtZXNzYWdlOiAnRWxpZ2UgZMOzbmRlIGd1YXJkYXIgZWwgUERGLicgfTsKICAgICAgfSBjYXRjaCAoZXJyb3IpIHsgcmV0dXJuIHsgc3VjY2VzczogZmFsc2UsIG1lc3NhZ2U6IGVycm9yLm1lc3NhZ2UgfTsgfQogICAgfQogICAgaWYgKHR5cGVvZiB3aW5kb3cuc2hvd1NhdmVGaWxlUGlja2VyID09PSAnZnVuY3Rpb24nKSB7CiAgICAgIHRyeSB7CiAgICAgICAgY29uc3QgaGFuZGxlID0gYXdhaXQgd2luZG93LnNob3dTYXZlRmlsZVBpY2tlcih7CiAgICAgICAgICBzdWdnZXN0ZWROYW1lOiBmaWxlTmFtZSwKICAgICAgICAgIHR5cGVzOiBbeyBkZXNjcmlwdGlvbjogJ1BERicsIGFjY2VwdDogeyAnYXBwbGljYXRpb24vcGRmJzogWycucGRmJ10gfSB9XQogICAgICAgIH0pOwogICAgICAgIGNvbnN0IHdyaXRlciA9IGF3YWl0IGhhbmRsZS5jcmVhdGVXcml0YWJsZSgpOwogICAgICAgIGF3YWl0IHdyaXRlci53cml0ZShibG9iKTsKICAgICAgICBhd2FpdCB3cml0ZXIuY2xvc2UoKTsKICAgICAgICByZXR1cm4geyBzdWNjZXNzOiB0cnVlLCBtZXRob2Q6ICdmaWxlX3BpY2tlcicsIG1lc3NhZ2U6ICdQREYgZ3VhcmRhZG8gY29ycmVjdGFtZW50ZS4nIH07CiAgICAgIH0gY2F0Y2ggKGVycm9yKSB7CiAgICAgICAgaWYgKGVycm9yPy5uYW1lID09PSAnQWJvcnRFcnJvcicpIHJldHVybiB7IHN1Y2Nlc3M6IGZhbHNlLCBjYW5jZWxsZWQ6IHRydWUgfTsKICAgICAgICByZXR1cm4geyBzdWNjZXNzOiBmYWxzZSwgbWVzc2FnZTogJ0Vycm9yIGFsIGd1YXJkYXIgZWwgUERGOiAnICsgZXJyb3IubWVzc2FnZSB9OwogICAgICB9CiAgICB9CiAgICB0aGlzLmRvd25sb2FkRmlsZShibG9iLCBmaWxlTmFtZSk7CiAgICByZXR1cm4geyBzdWNjZXNzOiBmYWxzZSwgcGVuZGluZzogdHJ1ZSwgbWV0aG9kOiAnZG93bmxvYWQnLCBtZXNzYWdlOiAnRGVzY2FyZ2EgaW5pY2lhZGE7IHZlcmlmaWNhIGVsIGFyY2hpdm8gZW4gRGVzY2FyZ2FzLicgfTsKICB9LAoKICBhc3luYyBzaGFyZVBkZk5hdGl2ZShibG9iLCBmaWxlTmFtZSwgbWV0YSA9IHt9LCBwcmVmZXJyZWQgPSAnJykgewogICAgaWYgKCEoYmxvYiBpbnN0YW5jZW9mIEJsb2IpIHx8ICFibG9iLnNpemUpIHJldHVybiB7IHN1Y2Nlc3M6IGZhbHNlLCBtZXNzYWdlOiAnTm8gaGF5IFBERiBwYXJhIGNvbXBhcnRpci4nIH07CiAgICBjb25zdCBzdW1tYXJ5ID0gdGhpcy5idWlsZFN1bW1hcnkobWV0YSwgZmlsZU5hbWUpOwogICAgaWYgKHdpbmRvdy5HcmVlbkFpck5hdGl2ZT8uc2hhcmVQZGYpIHsKICAgICAgdHJ5IHsKICAgICAgICB3aW5kb3cuR3JlZW5BaXJOYXRpdmUuc2hhcmVQZGYoYXdhaXQgdG9CYXNlNjQoYmxvYiksIGZpbGVOYW1lLCBzdW1tYXJ5LCBwcmVmZXJyZWQpOwogICAgICAgIHJldHVybiB7IHN1Y2Nlc3M6IGZhbHNlLCBwZW5kaW5nOiB0cnVlLCBtZXRob2Q6ICdhbmRyb2lkX25hdGl2ZScsIG1lc3NhZ2U6ICdQcmVwYXJhbmRvIGVsIHNlbGVjdG9yIG5hdGl2byBjb24gUERGIHkgdGV4dG8uJyB9OwogICAgICB9IGNhdGNoIChlcnJvcikgeyByZXR1cm4geyBzdWNjZXNzOiBmYWxzZSwgbWVzc2FnZTogZXJyb3IubWVzc2FnZSB9OyB9CiAgICB9CiAgICB0cnkgewogICAgICBjb25zdCBmaWxlID0gbmV3IEZpbGUoW2Jsb2JdLCBmaWxlTmFtZSwgeyB0eXBlOiAnYXBwbGljYXRpb24vcGRmJyB9KTsKICAgICAgaWYgKG5hdmlnYXRvci5jYW5TaGFyZT8uKHsgZmlsZXM6IFtmaWxlXSB9KSAmJiBuYXZpZ2F0b3Iuc2hhcmUpIHsKICAgICAgICBhd2FpdCBuYXZpZ2F0b3Iuc2hhcmUoeyB0aXRsZTogYEdyZWVuQWlyIFFDIOKAlCAke21ldGEub3JkZXJOdW1iZXIgfHwgbWV0YS5zZXJpYWxOdW1iZXIgfHwgJyd9YCwgdGV4dDogc3VtbWFyeSwgZmlsZXM6IFtmaWxlXSB9KTsKICAgICAgICByZXR1cm4geyBzdWNjZXNzOiB0cnVlLCBtZXRob2Q6ICd3ZWJfc2hhcmUnLCBtZXNzYWdlOiAnQXJjaGl2byBlbnRyZWdhZG8gYWwgc2lzdGVtYSBkZSBjb21wYXJ0aWNpw7NuOyBlbnbDrW8gbm8gY29uZmlybWFkby4nIH07CiAgICAgIH0KICAgIH0gY2F0Y2ggKGVycm9yKSB7CiAgICAgIGlmIChlcnJvcj8ubmFtZSA9PT0gJ0Fib3J0RXJyb3InKSByZXR1cm4geyBzdWNjZXNzOiBmYWxzZSwgY2FuY2VsbGVkOiB0cnVlIH07CiAgICAgIHJldHVybiB7IHN1Y2Nlc3M6IGZhbHNlLCBtZXNzYWdlOiAnTm8gc2UgcHVkbyBjb21wYXJ0aXI6ICcgKyBlcnJvci5tZXNzYWdlIH07CiAgICB9CiAgICByZXR1cm4geyBzdWNjZXNzOiBmYWxzZSwgdW5zdXBwb3J0ZWQ6IHRydWUsIG1lc3NhZ2U6ICdFc3RlIG5hdmVnYWRvciBubyBwZXJtaXRlIGFkanVudGFyIFBERiBhdXRvbcOhdGljYW1lbnRlLicgfTsKICB9LAoKICBhc3luYyBzaGFyZVdoYXRzQXBwKG1ldGEgPSB7fSwgZmlsZU5hbWUgPSAnJywgYmxvYiA9IG51bGwpIHsKICAgIGlmICghYmxvYikgcmV0dXJuIHsgc3VjY2VzczogZmFsc2UsIG1lc3NhZ2U6ICdHZW5lcmEgYW50ZXMgZWwgUERGLicgfTsKICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IHRoaXMuc2hhcmVQZGZOYXRpdmUoYmxvYiwgZmlsZU5hbWUsIG1ldGEsICd3aGF0c2FwcCcpOwogICAgaWYgKCFyZXN1bHQudW5zdXBwb3J0ZWQpIHJldHVybiByZXN1bHQ7CiAgICB0aGlzLmRvd25sb2FkRmlsZShibG9iLCBmaWxlTmFtZSk7CiAgICB3aW5kb3cub3BlbihgaHR0cHM6Ly9hcGkud2hhdHNhcHAuY29tL3NlbmQ/dGV4dD0ke2VuY29kZVVSSUNvbXBvbmVudCh0aGlzLmJ1aWxkU3VtbWFyeShtZXRhLCBmaWxlTmFtZSkpfWAsICdfYmxhbmsnKTsKICAgIHJldHVybiB7IHN1Y2Nlc3M6IGZhbHNlLCBwZW5kaW5nOiB0cnVlLCBtZXNzYWdlOiAnQWJpZXJ0byBXaGF0c0FwcCBjb24gZWwgcmVzdW1lbi4gQWRqdW50YSBtYW51YWxtZW50ZSBlbCBQREYgZGVzY2FyZ2Fkby4nIH07CiAgfSwKCiAgYXN5bmMgc2hhcmVFbWFpbChtZXRhID0ge30sIGZpbGVOYW1lID0gJycsIGJsb2IgPSBudWxsKSB7CiAgICBpZiAoIWJsb2IpIHJldHVybiB7IHN1Y2Nlc3M6IGZhbHNlLCBtZXNzYWdlOiAnR2VuZXJhIGFudGVzIGVsIFBERi4nIH07CiAgICBjb25zdCByZXN1bHQgPSBhd2FpdCB0aGlzLnNoYXJlUGRmTmF0aXZlKGJsb2IsIGZpbGVOYW1lLCBtZXRhKTsKICAgIGlmICghcmVzdWx0LnVuc3VwcG9ydGVkKSByZXR1cm4gcmVzdWx0OwogICAgdGhpcy5kb3dubG9hZEZpbGUoYmxvYiwgZmlsZU5hbWUpOwogICAgY29uc3Qgc3ViamVjdCA9IGBHcmVlbkFpciBRQyDigJQgUGVkaWRvICR7bWV0YS5vcmRlck51bWJlciB8fCAnU0lOIFBFRElETyd9IOKAlCBTZXJpZSAke21ldGEuc2VyaWFsTnVtYmVyIHx8ICcnfWA7CiAgICB3aW5kb3cub3BlbihgbWFpbHRvOj9zdWJqZWN0PSR7ZW5jb2RlVVJJQ29tcG9uZW50KHN1YmplY3QpfSZib2R5PSR7ZW5jb2RlVVJJQ29tcG9uZW50KHRoaXMuYnVpbGRTdW1tYXJ5KG1ldGEsIGZpbGVOYW1lKSl9YCwgJ19zZWxmJyk7CiAgICByZXR1cm4geyBzdWNjZXNzOiBmYWxzZSwgcGVuZGluZzogdHJ1ZSwgbWVzc2FnZTogJ0NvcnJlbyBwcmVwYXJhZG8uIEFkanVudGEgbWFudWFsbWVudGUgZWwgUERGIGRlc2NhcmdhZG8uJyB9OwogIH0sCgogIGRvd25sb2FkRmlsZShibG9iLCBmaWxlTmFtZSkgewogICAgY29uc3QgdXJsID0gVVJMLmNyZWF0ZU9iamVjdFVSTChibG9iKTsKICAgIGNvbnN0IGFuY2hvciA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2EnKTsKICAgIGFuY2hvci5ocmVmID0gdXJsOwogICAgYW5jaG9yLmRvd25sb2FkID0gZmlsZU5hbWU7CiAgICBkb2N1bWVudC5ib2R5LmFwcGVuZENoaWxkKGFuY2hvcik7CiAgICBhbmNob3IuY2xpY2soKTsKICAgIGFuY2hvci5yZW1vdmUoKTsKICAgIHNldFRpbWVvdXQoKCkgPT4gVVJMLnJldm9rZU9iamVjdFVSTCh1cmwpLCAzMDAwMCk7CiAgfQp9Owo=', 'android/app/src/main/res/xml/file_paths.xml': 'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPHBhdGhzIHhtbG5zOmFuZHJvaWQ9Imh0dHA6Ly9zY2hlbWFzLmFuZHJvaWQuY29tL2Fway9yZXMvYW5kcm9pZCI+CiAgICA8Y2FjaGUtcGF0aCBuYW1lPSJzaGFyZWRfcGRmcyIgcGF0aD0ic2hhcmVkX3BkZnMvIiAvPgogICAgPGNhY2hlLXBhdGggbmFtZT0iY2FtZXJhIiBwYXRoPSJjYW1lcmEvIiAvPgo8L3BhdGhzPgo=', 'android/app/src/main/java/com/greenair/industrial/qc/MainActivity.java': 'cGFja2FnZSBjb20uZ3JlZW5haXIuaW5kdXN0cmlhbC5xYzsKCmltcG9ydCBhbmRyb2lkLmFubm90YXRpb24uU3VwcHJlc3NMaW50OwppbXBvcnQgYW5kcm9pZC5hcHAuQWN0aXZpdHk7CmltcG9ydCBhbmRyb2lkLmNvbnRlbnQuQ2xpcERhdGE7CmltcG9ydCBhbmRyb2lkLmNvbnRlbnQuSW50ZW50OwppbXBvcnQgYW5kcm9pZC5uZXQuVXJpOwppbXBvcnQgYW5kcm9pZC5vcy5CdW5kbGU7CmltcG9ydCBhbmRyb2lkLnByb3ZpZGVyLk1lZGlhU3RvcmU7CmltcG9ydCBhbmRyb2lkLnV0aWwuQmFzZTY0OwppbXBvcnQgYW5kcm9pZC51dGlsLkxvZzsKaW1wb3J0IGFuZHJvaWQud2Via2l0LkNvbnNvbGVNZXNzYWdlOwppbXBvcnQgYW5kcm9pZC53ZWJraXQuSmF2YXNjcmlwdEludGVyZmFjZTsKaW1wb3J0IGFuZHJvaWQud2Via2l0LlZhbHVlQ2FsbGJhY2s7CmltcG9ydCBhbmRyb2lkLndlYmtpdC5XZWJDaHJvbWVDbGllbnQ7CmltcG9ydCBhbmRyb2lkLndlYmtpdC5XZWJSZXNvdXJjZVJlcXVlc3Q7CmltcG9ydCBhbmRyb2lkLndlYmtpdC5XZWJSZXNvdXJjZVJlc3BvbnNlOwppbXBvcnQgYW5kcm9pZC53ZWJraXQuV2ViU2V0dGluZ3M7CmltcG9ydCBhbmRyb2lkLndlYmtpdC5XZWJWaWV3OwppbXBvcnQgYW5kcm9pZC53ZWJraXQuV2ViVmlld0NsaWVudDsKaW1wb3J0IGFuZHJvaWQud2lkZ2V0LlRvYXN0OwppbXBvcnQgYW5kcm9pZHguYWN0aXZpdHkuQ29tcG9uZW50QWN0aXZpdHk7CmltcG9ydCBhbmRyb2lkeC5hbm5vdGF0aW9uLk51bGxhYmxlOwppbXBvcnQgYW5kcm9pZHguY29yZS5jb250ZW50LkZpbGVQcm92aWRlcjsKaW1wb3J0IGFuZHJvaWR4LndlYmtpdC5XZWJWaWV3QXNzZXRMb2FkZXI7CmltcG9ydCBqYXZhLmlvLkZpbGU7CmltcG9ydCBqYXZhLmlvLkZpbGVPdXRwdXRTdHJlYW07CmltcG9ydCBqYXZhLmlvLk91dHB1dFN0cmVhbTsKaW1wb3J0IG9yZy5qc29uLkpTT05PYmplY3Q7CgpwdWJsaWMgY2xhc3MgTWFpbkFjdGl2aXR5IGV4dGVuZHMgQ29tcG9uZW50QWN0aXZpdHkgewogICAgcHJpdmF0ZSBzdGF0aWMgZmluYWwgU3RyaW5nIFRBRyA9ICJHcmVlbkFpclFDIjsKICAgIHByaXZhdGUgc3RhdGljIGZpbmFsIFN0cmluZyBVUkwgPSAiaHR0cHM6Ly9hcHBhc3NldHMuYW5kcm9pZHBsYXRmb3JtLm5ldC9hc3NldHMvcHVibGljL2luZGV4Lmh0bWwiOwogICAgcHJpdmF0ZSBzdGF0aWMgZmluYWwgaW50IFBJQ0tfUEhPVE8gPSAyMDA7CiAgICBwcml2YXRlIHN0YXRpYyBmaW5hbCBpbnQgU0FWRV9QREYgPSAyMDE7CiAgICBwcml2YXRlIFdlYlZpZXcgd2ViVmlldzsKICAgIHByaXZhdGUgVmFsdWVDYWxsYmFjazxVcmlbXT4gcGVuZGluZ1Bob3RvczsKICAgIHByaXZhdGUgVXJpIGNhbWVyYU91dHB1dDsKICAgIHByaXZhdGUgYnl0ZVtdIHBkZlRvU2F2ZTsKICAgIHByaXZhdGUgU3RyaW5nIHBkZk5hbWVUb1NhdmU7CgogICAgQFN1cHByZXNzTGludCgiU2V0SmF2YVNjcmlwdEVuYWJsZWQiKQogICAgQE92ZXJyaWRlIHByb3RlY3RlZCB2b2lkIG9uQ3JlYXRlKEJ1bmRsZSBzdGF0ZSkgewogICAgICAgIHN1cGVyLm9uQ3JlYXRlKHN0YXRlKTsKICAgICAgICB3ZWJWaWV3ID0gbmV3IFdlYlZpZXcodGhpcyk7CiAgICAgICAgc2V0Q29udGVudFZpZXcod2ViVmlldyk7CiAgICAgICAgV2ViU2V0dGluZ3MgY2ZnID0gd2ViVmlldy5nZXRTZXR0aW5ncygpOwogICAgICAgIGNmZy5zZXRKYXZhU2NyaXB0RW5hYmxlZCh0cnVlKTsKICAgICAgICBjZmcuc2V0RG9tU3RvcmFnZUVuYWJsZWQodHJ1ZSk7CiAgICAgICAgY2ZnLnNldEFsbG93RmlsZUFjY2VzcyhmYWxzZSk7CiAgICAgICAgY2ZnLnNldEFsbG93RmlsZUFjY2Vzc0Zyb21GaWxlVVJMcyhmYWxzZSk7CiAgICAgICAgY2ZnLnNldEFsbG93VW5pdmVyc2FsQWNjZXNzRnJvbUZpbGVVUkxzKGZhbHNlKTsKICAgICAgICBjZmcuc2V0QWxsb3dDb250ZW50QWNjZXNzKHRydWUpOwogICAgICAgIGNmZy5zZXRNaXhlZENvbnRlbnRNb2RlKFdlYlNldHRpbmdzLk1JWEVEX0NPTlRFTlRfTkVWRVJfQUxMT1cpOwoKICAgICAgICBXZWJWaWV3QXNzZXRMb2FkZXIgbG9hZGVyID0gbmV3IFdlYlZpZXdBc3NldExvYWRlci5CdWlsZGVyKCkKICAgICAgICAgICAgLmFkZFBhdGhIYW5kbGVyKCIvYXNzZXRzLyIsIG5ldyBXZWJWaWV3QXNzZXRMb2FkZXIuQXNzZXRzUGF0aEhhbmRsZXIodGhpcykpCiAgICAgICAgICAgIC5idWlsZCgpOwogICAgICAgIHdlYlZpZXcuc2V0V2ViVmlld0NsaWVudChuZXcgV2ViVmlld0NsaWVudCgpIHsKICAgICAgICAgICAgQE92ZXJyaWRlIHB1YmxpYyBXZWJSZXNvdXJjZVJlc3BvbnNlIHNob3VsZEludGVyY2VwdFJlcXVlc3QoV2ViVmlldyB2aWV3LCBXZWJSZXNvdXJjZVJlcXVlc3QgcmVxdWVzdCkgewogICAgICAgICAgICAgICAgcmV0dXJuIGxvYWRlci5zaG91bGRJbnRlcmNlcHRSZXF1ZXN0KHJlcXVlc3QuZ2V0VXJsKCkpOwogICAgICAgICAgICB9CiAgICAgICAgICAgIEBPdmVycmlkZSBwdWJsaWMgYm9vbGVhbiBzaG91bGRPdmVycmlkZVVybExvYWRpbmcoV2ViVmlldyB2aWV3LCBXZWJSZXNvdXJjZVJlcXVlc3QgcmVxdWVzdCkgewogICAgICAgICAgICAgICAgVXJpIHVybCA9IHJlcXVlc3QuZ2V0VXJsKCk7CiAgICAgICAgICAgICAgICBpZiAoImFwcGFzc2V0cy5hbmRyb2lkcGxhdGZvcm0ubmV0Ii5lcXVhbHModXJsLmdldEhvc3QoKSkpIHJldHVybiBmYWxzZTsKICAgICAgICAgICAgICAgIHRyeSB7IHN0YXJ0QWN0aXZpdHkobmV3IEludGVudChJbnRlbnQuQUNUSU9OX1ZJRVcsIHVybCkpOyB9CiAgICAgICAgICAgICAgICBjYXRjaCAoRXhjZXB0aW9uIGV4KSB7IExvZy53KFRBRywgIk5vIHNlIHB1ZWRlIGFicmlyIGVubGFjZSBleHRlcm5vIiwgZXgpOyB9CiAgICAgICAgICAgICAgICByZXR1cm4gdHJ1ZTsKICAgICAgICAgICAgfQogICAgICAgIH0pOwogICAgICAgIHdlYlZpZXcuc2V0V2ViQ2hyb21lQ2xpZW50KG5ldyBXZWJDaHJvbWVDbGllbnQoKSB7CiAgICAgICAgICAgIEBPdmVycmlkZSBwdWJsaWMgYm9vbGVhbiBvbkNvbnNvbGVNZXNzYWdlKENvbnNvbGVNZXNzYWdlIG1zZykgewogICAgICAgICAgICAgICAgaWYgKChnZXRBcHBsaWNhdGlvbkluZm8oKS5mbGFncyAmIGFuZHJvaWQuY29udGVudC5wbS5BcHBsaWNhdGlvbkluZm8uRkxBR19ERUJVR0dBQkxFKSAhPSAwKSBMb2cuZChUQUcsICJKUyAiICsgbXNnLm1lc3NhZ2VMZXZlbCgpICsgIjogIiArIG1zZy5tZXNzYWdlKCkpOwogICAgICAgICAgICAgICAgcmV0dXJuIHRydWU7CiAgICAgICAgICAgIH0KICAgICAgICAgICAgQE92ZXJyaWRlIHB1YmxpYyBib29sZWFuIG9uU2hvd0ZpbGVDaG9vc2VyKFdlYlZpZXcgdmlldywgVmFsdWVDYWxsYmFjazxVcmlbXT4gY2FsbGJhY2ssIEZpbGVDaG9vc2VyUGFyYW1zIHBhcmFtcykgewogICAgICAgICAgICAgICAgaWYgKHBlbmRpbmdQaG90b3MgIT0gbnVsbCkgcGVuZGluZ1Bob3Rvcy5vblJlY2VpdmVWYWx1ZShudWxsKTsKICAgICAgICAgICAgICAgIHBlbmRpbmdQaG90b3MgPSBjYWxsYmFjazsKICAgICAgICAgICAgICAgIGNhbWVyYU91dHB1dCA9IG51bGw7CiAgICAgICAgICAgICAgICB0cnkgewogICAgICAgICAgICAgICAgICAgIGlmIChwYXJhbXMuaXNDYXB0dXJlRW5hYmxlZCgpKSB7CiAgICAgICAgICAgICAgICAgICAgICAgIEludGVudCBjYW1lcmEgPSBuZXcgSW50ZW50KE1lZGlhU3RvcmUuQUNUSU9OX0lNQUdFX0NBUFRVUkUpOwogICAgICAgICAgICAgICAgICAgICAgICBGaWxlIGZvbGRlciA9IG5ldyBGaWxlKGdldENhY2hlRGlyKCksICJjYW1lcmEiKTsKICAgICAgICAgICAgICAgICAgICAgICAgaWYgKCFmb2xkZXIuZXhpc3RzKCkgJiYgIWZvbGRlci5ta2RpcnMoKSkgdGhyb3cgbmV3IElsbGVnYWxTdGF0ZUV4Y2VwdGlvbigiTm8gc2UgY3Jlw7MgZGlyZWN0b3JpbyBkZSBjw6FtYXJhIik7CiAgICAgICAgICAgICAgICAgICAgICAgIEZpbGUgcGhvdG8gPSBGaWxlLmNyZWF0ZVRlbXBGaWxlKCJxY19waG90b18iLCAiLmpwZyIsIGZvbGRlcik7CiAgICAgICAgICAgICAgICAgICAgICAgIGNhbWVyYU91dHB1dCA9IEZpbGVQcm92aWRlci5nZXRVcmlGb3JGaWxlKE1haW5BY3Rpdml0eS50aGlzLCBnZXRQYWNrYWdlTmFtZSgpICsgIi5maWxlcyIsIHBob3RvKTsKICAgICAgICAgICAgICAgICAgICAgICAgY2FtZXJhLnB1dEV4dHJhKE1lZGlhU3RvcmUuRVhUUkFfT1VUUFVULCBjYW1lcmFPdXRwdXQpOwogICAgICAgICAgICAgICAgICAgICAgICBjYW1lcmEuc2V0Q2xpcERhdGEoQ2xpcERhdGEubmV3UmF3VXJpKCJGb3RvZ3JhZsOtYSIsIGNhbWVyYU91dHB1dCkpOwogICAgICAgICAgICAgICAgICAgICAgICBjYW1lcmEuYWRkRmxhZ3MoSW50ZW50LkZMQUdfR1JBTlRfUkVBRF9VUklfUEVSTUlTU0lPTiB8IEludGVudC5GTEFHX0dSQU5UX1dSSVRFX1VSSV9QRVJNSVNTSU9OKTsKICAgICAgICAgICAgICAgICAgICAgICAgc3RhcnRBY3Rpdml0eUZvclJlc3VsdChjYW1lcmEsIFBJQ0tfUEhPVE8pOwogICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7CiAgICAgICAgICAgICAgICAgICAgICAgIEludGVudCBwaWNrID0gbmV3IEludGVudChJbnRlbnQuQUNUSU9OX0dFVF9DT05URU5UKTsKICAgICAgICAgICAgICAgICAgICAgICAgcGljay5hZGRDYXRlZ29yeShJbnRlbnQuQ0FURUdPUllfT1BFTkFCTEUpOwogICAgICAgICAgICAgICAgICAgICAgICBwaWNrLnNldFR5cGUoImltYWdlLyoiKTsKICAgICAgICAgICAgICAgICAgICAgICAgcGljay5wdXRFeHRyYShJbnRlbnQuRVhUUkFfQUxMT1dfTVVMVElQTEUsIHBhcmFtcy5nZXRNb2RlKCkgPT0gRmlsZUNob29zZXJQYXJhbXMuTU9ERV9PUEVOX01VTFRJUExFKTsKICAgICAgICAgICAgICAgICAgICAgICAgc3RhcnRBY3Rpdml0eUZvclJlc3VsdChJbnRlbnQuY3JlYXRlQ2hvb3NlcihwaWNrLCAiU2VsZWNjaW9uYXIgZm90b2dyYWbDrWFzIiksIFBJQ0tfUEhPVE8pOwogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgICAgICByZXR1cm4gdHJ1ZTsKICAgICAgICAgICAgICAgIH0gY2F0Y2ggKEV4Y2VwdGlvbiBleCkgewogICAgICAgICAgICAgICAgICAgIExvZy5lKFRBRywgIk5vIHNlIHB1ZG8gYWJyaXIgY8OhbWFyYSBvIGdhbGVyw61hIiwgZXgpOwogICAgICAgICAgICAgICAgICAgIGNhbGxiYWNrLm9uUmVjZWl2ZVZhbHVlKG51bGwpOwogICAgICAgICAgICAgICAgICAgIHBlbmRpbmdQaG90b3MgPSBudWxsOwogICAgICAgICAgICAgICAgICAgIGNhbWVyYU91dHB1dCA9IG51bGw7CiAgICAgICAgICAgICAgICAgICAgVG9hc3QubWFrZVRleHQoTWFpbkFjdGl2aXR5LnRoaXMsICJObyBzZSBwdWRvIGFicmlyIGPDoW1hcmEgbyBhcmNoaXZvcyIsIFRvYXN0LkxFTkdUSF9MT05HKS5zaG93KCk7CiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHRydWU7CiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgIH0KICAgICAgICB9KTsKICAgICAgICAvLyBPbmx5IGJ1bmRsZWQgcGFnZSByZWNlaXZlcyB0aGUgbmF0aXZlIEFQSS4gTmV2ZXIgZW5hYmxlIHVuaXZlcnNhbCBmaWxlLW9yaWdpbiBhY2Nlc3MuCiAgICAgICAgd2ViVmlldy5hZGRKYXZhc2NyaXB0SW50ZXJmYWNlKG5ldyBOYXRpdmVCcmlkZ2UoKSwgIkdyZWVuQWlyTmF0aXZlIik7CiAgICAgICAgd2ViVmlldy5sb2FkVXJsKFVSTCk7CiAgICB9CgogICAgcHJpdmF0ZSBTdHJpbmcgc2FmZU5hbWUoU3RyaW5nIG5hbWUpIHsKICAgICAgICBTdHJpbmcgdmFsdWUgPSBuYW1lID09IG51bGwgPyAiRmljaGFfR3JlZW5BaXIucGRmIiA6IG5hbWUucmVwbGFjZUFsbCgiW15hLXpBLVowLTkuXy1dIiwgIl8iKTsKICAgICAgICBpZiAoIXZhbHVlLmVuZHNXaXRoKCIucGRmIikpIHZhbHVlICs9ICIucGRmIjsKICAgICAgICByZXR1cm4gdmFsdWUubGVuZ3RoKCkgPiAxNjAgPyB2YWx1ZS5zdWJzdHJpbmcoMCwgMTU2KSArICIucGRmIiA6IHZhbHVlOwogICAgfQoKICAgIHByaXZhdGUgdm9pZCBub3RpZnlKYXZhc2NyaXB0KFN0cmluZyBhY3Rpb24sIGJvb2xlYW4gc3VjY2VzcywgU3RyaW5nIG1lc3NhZ2UpIHsKICAgICAgICBydW5PblVpVGhyZWFkKCgpIC0+IHsKICAgICAgICAgICAgU3RyaW5nIGpzID0gIndpbmRvdy5kaXNwYXRjaEV2ZW50KG5ldyBDdXN0b21FdmVudCgnZ3JlZW5haXI6bmF0aXZlLXN0YXR1cycse2RldGFpbDp7YWN0aW9uOiIKICAgICAgICAgICAgICAgICsgSlNPTk9iamVjdC5xdW90ZShhY3Rpb24pICsgIixzdWNjZXNzOiIgKyBzdWNjZXNzICsgIixtZXNzYWdlOiIgKyBKU09OT2JqZWN0LnF1b3RlKG1lc3NhZ2UpICsgIn19KSkiOwogICAgICAgICAgICB3ZWJWaWV3LmV2YWx1YXRlSmF2YXNjcmlwdChqcywgbnVsbCk7CiAgICAgICAgICAgIFRvYXN0Lm1ha2VUZXh0KE1haW5BY3Rpdml0eS50aGlzLCBtZXNzYWdlLCBUb2FzdC5MRU5HVEhfTE9ORykuc2hvdygpOwogICAgICAgIH0pOwogICAgfQoKICAgIHByaXZhdGUgZmluYWwgY2xhc3MgTmF0aXZlQnJpZGdlIHsKICAgICAgICBASmF2YXNjcmlwdEludGVyZmFjZSBwdWJsaWMgdm9pZCBzaGFyZVBkZihTdHJpbmcgYmFzZTY0LCBTdHJpbmcgbmFtZSwgU3RyaW5nIHN1bW1hcnksIFN0cmluZyBwcmVmZXJyZWQpIHsKICAgICAgICAgICAgbmV3IFRocmVhZCgoKSAtPiB7CiAgICAgICAgICAgICAgICB0cnkgewogICAgICAgICAgICAgICAgICAgIGJ5dGVbXSBieXRlcyA9IEJhc2U2NC5kZWNvZGUoYmFzZTY0LCBCYXNlNjQuREVGQVVMVCk7CiAgICAgICAgICAgICAgICAgICAgaWYgKGJ5dGVzLmxlbmd0aCA8IDUgfHwgYnl0ZXNbMF0gIT0gJyUnIHx8IGJ5dGVzWzFdICE9ICdQJyB8fCBieXRlc1syXSAhPSAnRCcgfHwgYnl0ZXNbM10gIT0gJ0YnKSB0aHJvdyBuZXcgSWxsZWdhbEFyZ3VtZW50RXhjZXB0aW9uKCJBcmNoaXZvIFBERiBpbnbDoWxpZG8iKTsKICAgICAgICAgICAgICAgICAgICBGaWxlIGRpciA9IG5ldyBGaWxlKGdldENhY2hlRGlyKCksICJzaGFyZWRfcGRmcyIpOwogICAgICAgICAgICAgICAgICAgIGlmICghZGlyLmV4aXN0cygpICYmICFkaXIubWtkaXJzKCkpIHRocm93IG5ldyBJbGxlZ2FsU3RhdGVFeGNlcHRpb24oIk5vIHNlIHB1ZG8gY3JlYXIgYWxtYWNlbmFtaWVudG8gdGVtcG9yYWwiKTsKICAgICAgICAgICAgICAgICAgICBGaWxlIGZpbGUgPSBuZXcgRmlsZShkaXIsIHNhZmVOYW1lKG5hbWUpKTsKICAgICAgICAgICAgICAgICAgICB0cnkgKEZpbGVPdXRwdXRTdHJlYW0gc3RyZWFtID0gbmV3IEZpbGVPdXRwdXRTdHJlYW0oZmlsZSkpIHsgc3RyZWFtLndyaXRlKGJ5dGVzKTsgfQogICAgICAgICAgICAgICAgICAgIFVyaSB1cmkgPSBGaWxlUHJvdmlkZXIuZ2V0VXJpRm9yRmlsZShNYWluQWN0aXZpdHkudGhpcywgZ2V0UGFja2FnZU5hbWUoKSArICIuZmlsZXMiLCBmaWxlKTsKICAgICAgICAgICAgICAgICAgICBydW5PblVpVGhyZWFkKCgpIC0+IHsKICAgICAgICAgICAgICAgICAgICAgICAgdHJ5IHsKICAgICAgICAgICAgICAgICAgICAgICAgICAgIEludGVudCBpbnRlbnQgPSBuZXcgSW50ZW50KEludGVudC5BQ1RJT05fU0VORCk7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpbnRlbnQuc2V0VHlwZSgiYXBwbGljYXRpb24vcGRmIik7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpbnRlbnQucHV0RXh0cmEoSW50ZW50LkVYVFJBX1NUUkVBTSwgdXJpKTsKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGludGVudC5wdXRFeHRyYShJbnRlbnQuRVhUUkFfVEVYVCwgc3VtbWFyeSk7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpbnRlbnQuc2V0Q2xpcERhdGEoQ2xpcERhdGEubmV3UmF3VXJpKCJHcmVlbkFpciBQREYiLCB1cmkpKTsKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGludGVudC5hZGRGbGFncyhJbnRlbnQuRkxBR19HUkFOVF9SRUFEX1VSSV9QRVJNSVNTSU9OKTsKICAgICAgICAgICAgICAgICAgICAgICAgICAgIC8vIFdoYXRzQXBwIHNvbWV0aW1lcyBkaXNjYXJkcyBFWFRSQV9URVhUIHdpdGggUERGOyBPUy9wcm92aWRlciBkZWNpZGVzLgogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgKCJ3aGF0c2FwcCIuZXF1YWxzKHByZWZlcnJlZCkpIGludGVudC5zZXRQYWNrYWdlKCJjb20ud2hhdHNhcHAiKTsKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRyeSB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc3RhcnRBY3Rpdml0eShJbnRlbnQuY3JlYXRlQ2hvb3NlcihpbnRlbnQsICJDb21wYXJ0aXIgZmljaGEgUERGIikpOwogICAgICAgICAgICAgICAgICAgICAgICAgICAgfSBjYXRjaCAoRXhjZXB0aW9uIHdoYXRzYXBwVW5hdmFpbGFibGUpIHsKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpbnRlbnQuc2V0UGFja2FnZShudWxsKTsKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzdGFydEFjdGl2aXR5KEludGVudC5jcmVhdGVDaG9vc2VyKGludGVudCwgIkNvbXBhcnRpciBmaWNoYSBQREYiKSk7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICBub3RpZnlKYXZhc2NyaXB0KCJzaGFyZSIsIHRydWUsICJQREYgZW52aWFkbyBhbCBzZWxlY3RvcjsgY29uZmlybWEgZWwgZW52w61vIGVuIGxhIG90cmEgYXBsaWNhY2nDs24uIik7CiAgICAgICAgICAgICAgICAgICAgICAgIH0gY2F0Y2ggKEV4Y2VwdGlvbiBleCkgewogICAgICAgICAgICAgICAgICAgICAgICAgICAgTG9nLmUoVEFHLCAiTm8gc2UgcHVkbyBjb21wYXJ0aXIgUERGIiwgZXgpOwogICAgICAgICAgICAgICAgICAgICAgICAgICAgbm90aWZ5SmF2YXNjcmlwdCgic2hhcmUiLCBmYWxzZSwgIk5vIHNlIHB1ZG8gYWJyaXIgZWwgc2VsZWN0b3IgZGUgYXBsaWNhY2lvbmVzLiIpOwogICAgICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICAgICAgfSk7CiAgICAgICAgICAgICAgICB9IGNhdGNoIChFeGNlcHRpb24gZXgpIHsKICAgICAgICAgICAgICAgICAgICBMb2cuZShUQUcsICJObyBzZSBwdWRvIHByZXBhcmFyIFBERiIsIGV4KTsKICAgICAgICAgICAgICAgICAgICBub3RpZnlKYXZhc2NyaXB0KCJzaGFyZSIsIGZhbHNlLCAiTm8gc2UgcHVkbyBwcmVwYXJhciBlbCBkb2N1bWVudG8gUERGLiIpOwogICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9KS5zdGFydCgpOwogICAgICAgIH0KCiAgICAgICAgQEphdmFzY3JpcHRJbnRlcmZhY2UgcHVibGljIHZvaWQgc2F2ZVBkZihTdHJpbmcgYmFzZTY0LCBTdHJpbmcgbmFtZSkgewogICAgICAgICAgICBuZXcgVGhyZWFkKCgpIC0+IHsKICAgICAgICAgICAgICAgIHRyeSB7CiAgICAgICAgICAgICAgICAgICAgYnl0ZVtdIGJ5dGVzID0gQmFzZTY0LmRlY29kZShiYXNlNjQsIEJhc2U2NC5ERUZBVUxUKTsKICAgICAgICAgICAgICAgICAgICBpZiAoYnl0ZXMubGVuZ3RoIDwgNSB8fCBieXRlc1swXSAhPSAnJScgfHwgYnl0ZXNbMV0gIT0gJ1AnIHx8IGJ5dGVzWzJdICE9ICdEJyB8fCBieXRlc1szXSAhPSAnRicpIHRocm93IG5ldyBJbGxlZ2FsQXJndW1lbnRFeGNlcHRpb24oIlBERiBpbnbDoWxpZG8iKTsKICAgICAgICAgICAgICAgICAgICBydW5PblVpVGhyZWFkKCgpIC0+IHsKICAgICAgICAgICAgICAgICAgICAgICAgcGRmVG9TYXZlID0gYnl0ZXM7CiAgICAgICAgICAgICAgICAgICAgICAgIHBkZk5hbWVUb1NhdmUgPSBzYWZlTmFtZShuYW1lKTsKICAgICAgICAgICAgICAgICAgICAgICAgSW50ZW50IHNhdmUgPSBuZXcgSW50ZW50KEludGVudC5BQ1RJT05fQ1JFQVRFX0RPQ1VNRU5UKTsKICAgICAgICAgICAgICAgICAgICAgICAgc2F2ZS5hZGRDYXRlZ29yeShJbnRlbnQuQ0FURUdPUllfT1BFTkFCTEUpOwogICAgICAgICAgICAgICAgICAgICAgICBzYXZlLnNldFR5cGUoImFwcGxpY2F0aW9uL3BkZiIpOwogICAgICAgICAgICAgICAgICAgICAgICBzYXZlLnB1dEV4dHJhKEludGVudC5FWFRSQV9USVRMRSwgcGRmTmFtZVRvU2F2ZSk7CiAgICAgICAgICAgICAgICAgICAgICAgIHRyeSB7IHN0YXJ0QWN0aXZpdHlGb3JSZXN1bHQoc2F2ZSwgU0FWRV9QREYpOyB9CiAgICAgICAgICAgICAgICAgICAgICAgIGNhdGNoIChFeGNlcHRpb24gZSkgewogICAgICAgICAgICAgICAgICAgICAgICAgICAgcGRmVG9TYXZlID0gbnVsbDsKICAgICAgICAgICAgICAgICAgICAgICAgICAgIG5vdGlmeUphdmFzY3JpcHQoInNhdmUiLCBmYWxzZSwgIk5vIHNlIHB1ZG8gYWJyaXIgZWwgc2VsZWN0b3IgcGFyYSBndWFyZGFyLiIpOwogICAgICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICAgICAgfSk7CiAgICAgICAgICAgICAgICB9IGNhdGNoIChFeGNlcHRpb24gZXgpIHsKICAgICAgICAgICAgICAgICAgICBub3RpZnlKYXZhc2NyaXB0KCJzYXZlIiwgZmFsc2UsICJObyBzZSBwdWRvIHByZXBhcmFyIGVsIFBERiBwYXJhIGd1YXJkYXIuIik7CiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgIH0pLnN0YXJ0KCk7CiAgICAgICAgfQogICAgfQoKICAgIEBPdmVycmlkZSBwcm90ZWN0ZWQgdm9pZCBvbkFjdGl2aXR5UmVzdWx0KGludCBjb2RlLCBpbnQgcmVzdWx0LCBATnVsbGFibGUgSW50ZW50IGRhdGEpIHsKICAgICAgICBzdXBlci5vbkFjdGl2aXR5UmVzdWx0KGNvZGUsIHJlc3VsdCwgZGF0YSk7CiAgICAgICAgaWYgKGNvZGUgPT0gUElDS19QSE9UTykgewogICAgICAgICAgICBpZiAocGVuZGluZ1Bob3RvcyA9PSBudWxsKSByZXR1cm47CiAgICAgICAgICAgIFVyaVtdIGZpbGVzID0gbnVsbDsKICAgICAgICAgICAgaWYgKHJlc3VsdCA9PSBBY3Rpdml0eS5SRVNVTFRfT0spIHsKICAgICAgICAgICAgICAgIGlmIChkYXRhICE9IG51bGwgJiYgZGF0YS5nZXRDbGlwRGF0YSgpICE9IG51bGwpIHsKICAgICAgICAgICAgICAgICAgICBDbGlwRGF0YSBjbGlwcyA9IGRhdGEuZ2V0Q2xpcERhdGEoKTsKICAgICAgICAgICAgICAgICAgICBmaWxlcyA9IG5ldyBVcmlbY2xpcHMuZ2V0SXRlbUNvdW50KCldOwogICAgICAgICAgICAgICAgICAgIGZvciAoaW50IGkgPSAwOyBpIDwgY2xpcHMuZ2V0SXRlbUNvdW50KCk7IGkrKykgZmlsZXNbaV0gPSBjbGlwcy5nZXRJdGVtQXQoaSkuZ2V0VXJpKCk7CiAgICAgICAgICAgICAgICB9IGVsc2UgaWYgKGRhdGEgIT0gbnVsbCAmJiBkYXRhLmdldERhdGEoKSAhPSBudWxsKSB7CiAgICAgICAgICAgICAgICAgICAgZmlsZXMgPSBuZXcgVXJpW117IGRhdGEuZ2V0RGF0YSgpIH07CiAgICAgICAgICAgICAgICB9IGVsc2UgaWYgKGNhbWVyYU91dHB1dCAhPSBudWxsKSB7CiAgICAgICAgICAgICAgICAgICAgZmlsZXMgPSBuZXcgVXJpW117IGNhbWVyYU91dHB1dCB9OwogICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9CiAgICAgICAgICAgIHBlbmRpbmdQaG90b3Mub25SZWNlaXZlVmFsdWUoZmlsZXMpOwogICAgICAgICAgICBwZW5kaW5nUGhvdG9zID0gbnVsbDsKICAgICAgICAgICAgY2FtZXJhT3V0cHV0ID0gbnVsbDsKICAgICAgICB9CiAgICAgICAgaWYgKGNvZGUgPT0gU0FWRV9QREYpIHsKICAgICAgICAgICAgYnl0ZVtdIGJ5dGVzID0gcGRmVG9TYXZlOwogICAgICAgICAgICBwZGZUb1NhdmUgPSBudWxsOwogICAgICAgICAgICBpZiAocmVzdWx0ID09IEFjdGl2aXR5LlJFU1VMVF9PSyAmJiBkYXRhICE9IG51bGwgJiYgZGF0YS5nZXREYXRhKCkgIT0gbnVsbCAmJiBieXRlcyAhPSBudWxsKSB7CiAgICAgICAgICAgICAgICB0cnkgKE91dHB1dFN0cmVhbSBzdHJlYW0gPSBnZXRDb250ZW50UmVzb2x2ZXIoKS5vcGVuT3V0cHV0U3RyZWFtKGRhdGEuZ2V0RGF0YSgpKSkgewogICAgICAgICAgICAgICAgICAgIGlmIChzdHJlYW0gPT0gbnVsbCkgdGhyb3cgbmV3IElsbGVnYWxTdGF0ZUV4Y2VwdGlvbigiRGVzdGlubyBpbmFjY2VzaWJsZSIpOwogICAgICAgICAgICAgICAgICAgIHN0cmVhbS53cml0ZShieXRlcyk7CiAgICAgICAgICAgICAgICAgICAgc3RyZWFtLmZsdXNoKCk7CiAgICAgICAgICAgICAgICAgICAgbm90aWZ5SmF2YXNjcmlwdCgic2F2ZSIsIHRydWUsICJQREYgZ3VhcmRhZG8gY29ycmVjdGFtZW50ZS4iKTsKICAgICAgICAgICAgICAgIH0gY2F0Y2ggKEV4Y2VwdGlvbiBleCkgewogICAgICAgICAgICAgICAgICAgIExvZy5lKFRBRywgIk5vIHNlIHB1ZG8gZ3VhcmRhciBQREYiLCBleCk7CiAgICAgICAgICAgICAgICAgICAgbm90aWZ5SmF2YXNjcmlwdCgic2F2ZSIsIGZhbHNlLCAiRXJyb3IgYWwgZXNjcmliaXIgZWwgUERGLiIpOwogICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9IGVsc2UgewogICAgICAgICAgICAgICAgbm90aWZ5SmF2YXNjcmlwdCgic2F2ZSIsIGZhbHNlLCAiR3VhcmRhZG8gY2FuY2VsYWRvLCBlbCBQREYgbm8gc2UgZWxpbWluw7MuIik7CiAgICAgICAgICAgIH0KICAgICAgICB9CiAgICB9CgogICAgQE92ZXJyaWRlIHByb3RlY3RlZCB2b2lkIG9uRGVzdHJveSgpIHsKICAgICAgICBpZiAocGVuZGluZ1Bob3RvcyAhPSBudWxsKSBwZW5kaW5nUGhvdG9zLm9uUmVjZWl2ZVZhbHVlKG51bGwpOwogICAgICAgIGlmICh3ZWJWaWV3ICE9IG51bGwpIHdlYlZpZXcuZGVzdHJveSgpOwogICAgICAgIHN1cGVyLm9uRGVzdHJveSgpOwogICAgfQp9Cg=='}

def load(path):
    f=root/path
    if not f.is_file(): raise RuntimeError(f'Falta archivo requerido: {f}')
    return f.read_text(encoding='utf-8-sig')

def put(path,content): modified[path]=content

def repl(src,old,new,desc):
    if old not in src: raise RuntimeError(f'No se encontró {desc}. Tal vez el repositorio cambió; no se aplicarán cambios incompletos.')
    return src.replace(old,new,1)

def regex(src,pattern,replacement,desc,flags=re.S):
    result,count=re.subn(pattern,replacement,src,count=1,flags=flags)
    if count!=1: raise RuntimeError(f'No se encontró estructura {desc}')
    return result

html=load('index.html')
html=regex(html,r'\s*<button\b[^>]*id="btnRealPlatePhoto".*?</button>','', 'demo foto GISER')
html=regex(html,r'\s*<button\b[^>]*id="btnSamplePlate".*?</button>','', 'demo placa sintética')
html=repl(html,'<div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 mb-4">','<div class="grid grid-cols-1 gap-2.5 mb-4">','fila botones OCR')
html=repl(html,'<div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">','''<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
          <div>
            <label for="orderInput" class="block text-xs font-bold text-slate-700 mb-1">Número de Pedido <span class="text-red-500">*</span></label>
            <input type="text" id="orderInput" required maxlength="100" autocomplete="off" placeholder="Ej: PED-2026-001" class="w-full px-3 py-2 text-sm font-semibold bg-slate-50 border border-slate-300 rounded-lg focus:bg-white focus:ring-2 focus:ring-emerald-500 focus:outline-none transition">
            <span class="text-[10px] text-slate-400">Carga manual: no se obtiene mediante OCR.</span>
          </div>''','insertar número pedido')
html=repl(html,'<div id="subSondaCo2Container" class="hidden mt-3 pt-2.5 border-t border-slate-200 pl-8">','''<div id="subSondaCo2Container" class="hidden mt-3 pt-2.5 border-t border-slate-200 pl-8">
              <div class="mb-3">
                <label for="selectSondaCo2" class="block text-xs font-bold text-slate-700 mb-1">Tipo de sonda de CO₂ <span class="text-red-500">*</span></label>
                <div class="flex flex-wrap items-center gap-2">
                  <select id="selectSondaCo2" class="flex-1 min-w-[130px] px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white"><option value="">-- Seleccionar tipo --</option></select>
                  <button type="button" data-add-role="sondaCo2" class="text-xs font-bold bg-emerald-100 text-emerald-900 px-3 py-2 rounded-lg">+ Añadir</button>
                  <button type="button" data-manage-role="sondaCo2" class="text-xs font-bold bg-slate-200 text-slate-800 px-3 py-2 rounded-lg">Gestionar</button>
                </div>
              </div>''','desplegable sonda CO2')
html=regex(html,r'<!-- Botones de Acción de Fotos -->.*?<!-- PHOTO GALLERY GRID -->','''<!-- Botones independientes: cámara y galería -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
          <label class="btn-press block cursor-pointer text-center bg-emerald-700 hover:bg-emerald-800 text-white font-bold py-3 px-4 rounded-xl">
            📷 Tomar fotografía
            <input id="photoCameraInput" type="file" accept="image/*" capture="environment" class="sr-only">
          </label>
          <label class="btn-press block cursor-pointer text-center bg-slate-200 hover:bg-slate-300 text-slate-900 font-bold py-3 px-4 rounded-xl">
            📁 Adjuntar evidencia
            <input id="photoInput" type="file" accept="image/*" multiple class="sr-only">
          </label>
        </div>
        <!-- PHOTO GALLERY GRID -->''','botones foto y demo')
html=repl(html,'<button type="button" id="btnSaveReport"','<button type="button" id="btnClearForm" class="btn-press shrink-0 rounded-xl border border-slate-300 bg-slate-100 text-slate-800 font-semibold text-xs p-3">LIMPIAR</button>\n        <button type="button" id="btnSaveReport"','botón limpiar')
html=regex(html,r'(<button\b[^>]*id="btnFinalizeAction"[^>]*>)\s*FINALIZAR',r'\1\n        NUEVA MÁQUINA','botón nueva máquina')
# Palette: emerald/forest, gray, white; amber only for secondary accents.
html=html.replace('from-sky-600 to-indigo-600','from-emerald-700 to-emerald-600').replace('from-sky-500 to-indigo-500','from-emerald-600 to-emerald-500')
html=html.replace('from-sky-700 to-indigo-700','from-emerald-800 to-emerald-700')
html=re.sub(r'(?<![a-zA-Z])sky-', 'emerald-', html)
html=html.replace('from-emerald-600 to-emerald-700','from-emerald-700 to-emerald-800')
html=html.replace('<meta name="theme-color" content="#0f172a">','<meta name="theme-color" content="#164e3a">')
html=html.replace('  <!-- Tailwind CSS CDN -->','  <!-- Tailwind CSS CDN: requiere Internet mientras no se empaquete localmente -->')
put('index.html',html)

st=load('js/storage.js')
st=repl(st,"  MONTADORES: 'qc_montadores',","  SONDAS_CO2: 'qc_sondas_co2',\n  MONTADORES: 'qc_montadores',",'clave storage sonda')
st=repl(st,"  configuraciones: ['Estándar'],","  configuraciones: [],",'configuraciones de ejemplo')
st=repl(st,"  montadores: ['Carlos Rodríguez', 'David Martínez', 'Alejandro Morales', 'Javier Gómez'],","  montadores: [],",'nombres demostración montadores')
st=repl(st,"  electricistas: ['Miguel Ángel Rivas', 'Andrés Mendoza', 'Laura Fernández', 'Víctor Hugo Peña']","  electricistas: []",'nombres demostración electricistas')
st=repl(st,"    // 3. Montadores","    if (!localStorage.getItem(STORAGE_KEYS.SONDAS_CO2)) localStorage.setItem(STORAGE_KEYS.SONDAS_CO2, JSON.stringify([]));\n    // 3. Montadores",'inicializacion sonda')
st=st.replace("      case 'electricista':\n        key = STORAGE_KEYS.ELECTRICISTAS;", "      case 'sondaCo2':\n        key = STORAGE_KEYS.SONDAS_CO2;\n        break;\n      case 'electricista':\n        key = STORAGE_KEYS.ELECTRICISTAS;")
st=repl(st,'        serialNumber: report.serialNumber,','        orderNumber: report.orderNumber || \'\',\n        serialNumber: report.serialNumber,','historial pedido')
put('js/storage.js',st)

app=load('js/app.js')
app=repl(app,'    this.currentPdfSizeBytes = 0;','    this.currentPdfSizeBytes = 0;\n    this.pdfWasSaved = false;','estado PDF')
app=repl(app,'    this.updatePhotoCounter();\n    console.log', '''    this.updatePhotoCounter();
    this.updateCheckpointBadges();
    window.addEventListener('greenair:native-status', (event) => {
      const detail = event.detail || {};
      if (detail.action === 'save' && detail.success) this.pdfWasSaved = true;
      this.showToast(detail.message || (detail.success ? 'Acción completada' : 'Acción cancelada'), detail.success ? 'success' : 'info');
    });
    console.log''','inicializar badges/native status')
# Remove demo event binding only; demo helper methods are left unused to avoid harming dependencies.
app=regex(app,r'\s*const btnSamplePlate = document.getElementById\(\'btnSamplePlate\'\);.*?\n    // 3. PHOTO EVIDENCE','\n    // 3. PHOTO EVIDENCE','binding demos OCR')
app=repl(app,"    const photoInput = document.getElementById('photoInput');", "    const photoCameraInput = document.getElementById('photoCameraInput');\n    photoCameraInput?.addEventListener('change', (e) => this.handlePhotoUpload(e));\n    const photoInput = document.getElementById('photoInput');",'binding camara')
app=regex(app,r'\s*const btnSamplePhotos = document.getElementById\(\'btnSamplePhotos\'\);.*?\n    // 4. CHECKPOINTS TOGGLE','\n    // 4. CHECKPOINTS TOGGLE','binding demo fotos')
app=repl(app,'    // Optional components toggles','''    const btnClear = document.getElementById('btnClearForm');
    btnClear?.addEventListener('click', () => {
      if (confirm('¿Borrar los datos de la máquina actual? Los cambios no guardados se perderán.')) this.resetMachineForm();
    });
    document.querySelectorAll('.checkpoint-card input[type="checkbox"]').forEach(cb => {
      cb.addEventListener('change', () => this.updateCheckpointBadges());
    });
    // Optional components toggles''','checkpoint y limpiar')
app=repl(app,"    this.showToast('Todos los checkpoints marcados como Correctos (OK)', 'success');", "    this.updateCheckpointBadges();\n    this.showToast('Todos los checkpoints marcados como Correctos (OK)', 'success');",'check all sync')
app=repl(app,"    for (const file of files) {", "    let photoErrors = 0;\n    for (const file of files) {", 'contador errores fotografias')
app=repl(app,"        console.error('Error al comprimir foto:', err);", "        console.error('Error al comprimir foto:', err);\n        photoErrors++;",'errores comprimir fotos')
app=repl(app,"    this.renderPhotoGallery();\n    this.updatePhotoCounter();\n    event.target.value = '';", "    this.renderPhotoGallery();\n    this.updatePhotoCounter();\n    if (photoErrors) this.showToast(`${photoErrors} fotografía(s) no pudieron adjuntarse. Prueba otra imagen.`, 'error');\n    else this.showToast(`${files.length} fotografía(s) adjuntadas.`, 'success');\n    event.target.value = '';",'avisar si fallo captura fotos')
app=repl(app,'  // ----------------------------------------------------\n  // DROPDOWNS MANAGEMENT', '''  updateCheckpointBadges() {
    document.querySelectorAll('.checkpoint-card').forEach(card => {
      const cb = card.querySelector('input[type="checkbox"]');
      if (!cb) return;
      const status = card.lastElementChild;
      if (!status || status.tagName !== 'SPAN') return;
      status.textContent = cb.checked ? 'Correcto' : 'Incorrecto';
      status.className = cb.checked
        ? 'qc-status text-xs font-semibold text-emerald-800 bg-emerald-100 px-2.5 py-1 rounded-md'
        : 'qc-status text-xs font-bold text-red-800 bg-red-100 border border-red-300 px-2.5 py-1 rounded-md';
      card.classList.toggle('checked', cb.checked);
    });
  }
  // ----------------------------------------------------
  // DROPDOWNS MANAGEMENT''','funcion badge')
app=repl(app,"    this.renderSingleDropdown('electricista', 'selectElectricista');", "    this.renderSingleDropdown('electricista', 'selectElectricista');\n    this.renderSingleDropdown('sondaCo2', 'selectSondaCo2');",'render dropdown sonda')
app=repl(app,"    if (!select.value && list.length > 0) {\n      select.selectedIndex = 1;\n    }", "    // No autoseleccionar valores: evita arrastrar un responsable de otra máquina.",'deshabilitar autoseleccion')
app=repl(app,"      electricista: {\n        title: 'Electricista',", "      sondaCo2: {\n        title: 'Tipo de Sonda CO2',\n        lbl: 'Nombre o código del tipo de sonda:',\n        placeholder: 'Introduce el tipo real de sonda'\n      },\n      electricista: {\n        title: 'Electricista',",'meta alta sonda')
app=repl(app,"      electricista: 'selectElectricista'", "      electricista: 'selectElectricista',\n      sondaCo2: 'selectSondaCo2'",'select map sonda')
app=repl(app,"      electricista: 'Gestionar Lista de Electricistas'", "      electricista: 'Gestionar Lista de Electricistas',\n      sondaCo2: 'Gestionar Tipos de Sonda CO2'",'titulo gestionar sonda')
app=repl(app,"    const configuracion = (document.getElementById('selectConfiguracion')?.value || 'Estándar').trim();", "    const configuracion = (document.getElementById('selectConfiguracion')?.value || '').trim();",'no inventar config')
app=repl(app,"    const cuadro = (document.getElementById('selectCuadro')?.value || 'GISER').trim();", "    const cuadro = (document.getElementById('selectCuadro')?.value || '').trim();",'no inventar cuadro')
app=repl(app,"    const serialNumber = (document.getElementById('serialInput')?.value || '').trim();", "    const orderNumber = (document.getElementById('orderInput')?.value || '').trim();\n    const serialNumber = (document.getElementById('serialInput')?.value || '').trim();",'extraer pedido')
app=repl(app,"      serialNumber,\n      fabricationDate,", "      serialNumber,\n      orderNumber,\n      fabricationDate,",'pedido en data')
app=repl(app,"sondaCo2: { has: hasSondaCo2, working: workingSondaCo2 }", "sondaCo2: { has: hasSondaCo2, working: workingSondaCo2, type: hasSondaCo2 ? (document.getElementById('selectSondaCo2')?.value || '') : '' }",'tipo sonda data')
app=repl(app,"  validateForm(data) {\n    if (!data.serialNumber)", "  validateForm(data) {\n    if (!data.orderNumber) {\n      this.showToast('El Número de Pedido es obligatorio.', 'error');\n      document.getElementById('orderInput')?.focus();\n      return false;\n    }\n    if (data.optionals.sondaCo2.has && !data.optionals.sondaCo2.type) {\n      this.showToast('Selecciona el tipo de Sonda CO2.', 'error');\n      document.getElementById('selectSondaCo2')?.focus();\n      return false;\n    }\n    if (!data.serialNumber)",'validacion pedido y sonda')
app=repl(app,'      this.currentPdfBlob = result.blob;', '      this.pdfWasSaved = false;\n      this.currentPdfBlob = result.blob;','estado pdf nuevo')
app=repl(app,'        serialNumber: data.serialNumber,', '        serialNumber: data.serialNumber,\n        orderNumber: data.orderNumber,','historial pedido app')
app=repl(app,'    if (labelSerial) labelSerial.innerText = `Nº Serie: ${data.serialNumber}`;', '    if (labelSerial) labelSerial.innerText = `Pedido: ${data.orderNumber} · Serie: ${data.serialNumber}`;','modal pedido')
app=repl(app,"    if (res.cancelled) {\n      this.showToast('Guardado cancelado por el usuario.', 'info');", "    if (res.cancelled) {\n      this.showToast('Guardado cancelado por el usuario.', 'info');",'ubicacion saved status')
app=repl(app,"    } else if (res.success) {\n      this.showToast(res.message || 'PDF guardado con éxito.', 'success');", "    } else if (res.success) {\n      this.pdfWasSaved = true;\n      this.showToast(res.message || 'PDF guardado con éxito.', 'success');",'guardado confirmado')
app=repl(app,"    } else {\n      this.showToast(res.message || 'Error al guardar el archivo.', 'error');\n    }\n  }\n  // 2. COMPARTIR", "    } else {\n      this.showToast(res.message || 'No se confirmó el guardado.', res.pending ? 'info' : 'error');\n    }\n  }\n  // 2. COMPARTIR",'guardado pendiente')
app=regex(app,r'  // 2\. COMPARTIR PDF \(Native file sharing\).*?  // ----------------------------------------------------\n  // TOAST NOTIFICATIONS', '''  // Compartir el archivo con un selector nativo en Android.
  async handleSharePdf() {
    if (!this.currentPdfBlob) return this.showToast('Primero genera el PDF.', 'error');
    const result = await ShareEngine.sharePdfNative(this.currentPdfBlob, this.currentPdfFileName, this.getFormData());
    if (result.unsupported) {
      ShareEngine.downloadFile(this.currentPdfBlob, this.currentPdfFileName);
      this.showToast('PDF descargado; adjúntalo manualmente desde tu aplicación.', 'warning');
    } else if (!result.cancelled) this.showToast(result.message || 'Compartición preparada.', result.pending ? 'info' : (result.success ? 'success' : 'error'));
  }
  async handleWhatsAppShare() {
    if (!this.currentPdfBlob) return this.showToast('Primero genera el PDF.', 'error');
    const result = await ShareEngine.shareWhatsApp(this.getFormData(), this.currentPdfFileName, this.currentPdfBlob);
    this.showToast(result.message || 'Selector abierto. Confirma el envío en WhatsApp.', result.unsupported ? 'warning' : 'info');
  }
  async handleGmailShare() {
    if (!this.currentPdfBlob) return this.showToast('Primero genera el PDF.', 'error');
    const result = await ShareEngine.shareEmail(this.getFormData(), this.currentPdfFileName, this.currentPdfBlob);
    this.showToast(result.message || 'Selector abierto. Confirma el envío.', 'info');
  }
  handleFinalizeProcess() {
    const message = this.pdfWasSaved
      ? '¿Comenzar una nueva máquina? La ficha actual se borrará del formulario.'
      : 'Aún no se ha confirmado el guardado del PDF. ¿Descartar los datos actuales y comenzar una nueva máquina?';
    if (!confirm(message)) return;
    this.resetMachineForm();
    this.closeShareModal();
    this.showToast('Formulario preparado para la siguiente máquina.', 'success');
  }
  resetMachineForm() {
    document.querySelectorAll('#viewElectricityScreen input, #viewElectricityScreen select, #viewElectricityScreen textarea').forEach(el => {
      if (el.matches('input[type="checkbox"]')) el.checked = false;
      else if (el.matches('input[type="file"]')) el.value = '';
      else if (el.tagName === 'SELECT') el.selectedIndex = 0;
      else el.value = '';
    });
    this.photos = [];
    this.renderPhotoGallery();
    this.updatePhotoCounter();
    this.updateCheckpointBadges();
    document.getElementById('platePreviewContainer')?.classList.add('hidden');
    const preview = document.getElementById('platePreviewImg');
    if (preview) preview.removeAttribute('src');
    document.getElementById('ocrStatusContainer')?.classList.add('hidden');
    document.getElementById('subSondaCo2Container')?.classList.add('hidden');
    document.getElementById('subMandoContainer')?.classList.add('hidden');
    this.currentPdfBlob = null;
    this.currentPdfFileName = '';
    this.currentPdfSizeBytes = 0;
    this.pdfWasSaved = false;
    document.getElementById('orderInput')?.focus();
    window.scrollTo({top:0, behavior:'smooth'});
  }
  // ----------------------------------------------------
  // TOAST NOTIFICATIONS''','compartir y limpiar')
# Avoid injecting user-controlled text as HTML in toast notification
app=repl(app,'    toast.innerHTML = `<span>${message}</span>`;','    const label = document.createElement(\'span\');\n    label.textContent = message;\n    toast.appendChild(label);','toast sin XSS')
put('js/app.js',app)

pdf=load('js/pdf-generator.js')
pdf=repl(pdf,"    const fileName = `${safeSerial}_Ficha_Pruebas.pdf`;", "    const safeOrder = (data.orderNumber || 'SIN_PEDIDO').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 60);\n    const fileName = `${safeOrder}_${safeSerial.slice(0,60)}_Ficha_Pruebas.pdf`;",'nombre pdf pedido serie')
pdf=repl(pdf,"    doc.roundedRect(margin, currentY, contentWidth, 34, 2, 2, 'F');", "    doc.roundedRect(margin, currentY, contentWidth, 42, 2, 2, 'F');",'altura ficha fondo')
pdf=repl(pdf,"    doc.roundedRect(margin, currentY, contentWidth, 34, 2, 2, 'S');", "    doc.roundedRect(margin, currentY, contentWidth, 42, 2, 2, 'S');",'altura ficha contorno')
pdf=repl(pdf,'    currentY += 39;', '''    doc.setFont('helvetica', 'bold');
    doc.setTextColor(71, 85, 105);
    doc.text('Nº PEDIDO:', margin + 4, currentY + 35);
    doc.setTextColor(14, 89, 60);
    doc.text(doc.splitTextToSize(data.orderNumber || 'SIN PEDIDO', 140)[0], margin + 30, currentY + 35);
    currentY += 47;''','pdf pedido tarjeta')
pdf=repl(pdf,"        desc: 'Sensor ambiental de ppm de CO2 con salida 0-10V'", "        desc: data.optionals?.sondaCo2?.has ? 'Tipo: ' + (data.optionals?.sondaCo2?.type || 'No especificado').slice(0, 28) : 'No instalada'",'tipo sonda pdf')
pdf=repl(pdf,"    // Right-aligned status stamp", "    const allOk = Object.values(data.checkpoints || {}).every(Boolean) && (!data.optionals?.sondaCo2?.has || data.optionals.sondaCo2.working) && (!data.optionals?.mandoSuperficie?.has || data.optionals.mandoSuperficie.working);\n    // Right-aligned status stamp",'calcular estado pdf')
pdf=repl(pdf,"    doc.text('ENSAYO OK', pageWidth - margin - 19, 14, { align: 'center' });", "    doc.text(allOk ? 'ENSAYO OK' : 'REVISAR', pageWidth - margin - 19, 14, { align: 'center' });",'status pdf real')
pdf=repl(pdf,"    doc.text('CONFORME A NORMA', pageWidth - margin - 19, 18, { align: 'center' });", "    doc.text(allOk ? 'VERIFICADO' : 'NO CONFORME', pageWidth - margin - 19, 18, { align: 'center' });",'pdf no afirmar conforms')
pdf=repl(pdf,"    doc.setFillColor(16, 185, 129); // emerald-500", "    doc.setFillColor(...(allOk ? [5, 150, 105] : [185, 28, 28]));",'color pdf status')
pdf=repl(pdf,"      doc.text('No se adjuntaron fotografías adicionales. Comprobación conforme a inspección técnica visual en banco de pruebas.', margin + 6, currentY + 7);", "      doc.text('No se adjuntaron fotografías de evidencia.', margin + 6, currentY + 7);",'sin conformidad ficticia')
pdf=repl(pdf,"      doc.text('Pruebas funcionales de presostatos, ventiladores y sondas térmicas validadas satisfactoriamente.', margin + 6, currentY + 11.5);", "      doc.text('Consultar resultados individuales en la tabla de checkpoints.', margin + 6, currentY + 11.5);",'sin afirmacion foto')
# Keep 1-3 photos on first page, extra photos on following pages rather than silently dropping them.
pdf=repl(pdf,'    // ----------------------------------------------------\n    // 7. FOOTER & COMPLIANCE', '''    if (photos.length > 3) {
      const remaining = photos.slice(3);
      remaining.forEach((photo, i) => {
        if (i % 6 === 0) {
          doc.addPage();
          doc.setFont('helvetica', 'bold');
          doc.setTextColor(15, 73, 53);
          doc.setFontSize(12);
          doc.text('GREENAIR QC — EVIDENCIA FOTOGRÁFICA', margin, 16);
          doc.setFontSize(8);
          doc.text(`Pedido ${data.orderNumber} | Serie ${data.serialNumber}`, margin, 23);
        }
        const slot = i % 6;
        const x = margin + (slot % 2) * 93;
        const y = 29 + Math.floor(slot / 2) * 78;
        try {
          doc.addImage(photo.dataUrl, 'JPEG', x, y, 88, 62, undefined, 'FAST');
          doc.setFont('helvetica', 'normal');
          doc.setTextColor(40, 60, 50);
          doc.setFontSize(7);
          doc.text(`Foto ${i + 4}: ${(photo.caption || 'Evidencia').slice(0, 50)}`, x, y + 68);
        } catch (e) { console.warn('Foto no incrustada:', e); }
      });
    }
    // ----------------------------------------------------
    // 7. FOOTER & COMPLIANCE''','fotos adicionales pdf')
pdf=repl(pdf,"    doc.text(`Registro Electrónico Nº ${safeSerial} | Página 1 de 1`, pageWidth - margin, footerY + 2, { align: 'right' });", "    const totalPages = doc.internal.getNumberOfPages();\n    doc.setPage(1);\n    doc.text(`Pedido ${safeOrder} | Serie ${safeSerial} | Página 1 de ${totalPages}`, pageWidth - margin, footerY + 2, { align: 'right' });\n    doc.setPage(totalPages);",'conteo paginas pdf')
pdf=pdf.replace('doc.setFillColor(15, 23, 42); // slate-900','doc.setFillColor(15, 73, 53); // verde GreenAir').replace('doc.setFillColor(2, 132, 199); // sky-600','doc.setFillColor(234, 130, 27); // naranja acento')
put('js/pdf-generator.js',pdf)

ocr=load('js/ocr.js')
ocr=repl(ocr,"        rawText = 'GSR26 15/20 H-M   27/10/2026   Nº 2209946';", "        throw new Error('El motor OCR no está disponible. Verifica la conexión e introduce los datos manualmente.');",'OCR no fabricar resultados')
ocr=repl(ocr,"      model: model || 'GSR26 15/20 H-M',", "      model: model || '',",'no fabricar modelo')
ocr=repl(ocr,"      serialNumber: serialNumber || '2209946',", "      serialNumber: serialNumber || '',",'no fabricar serial')
ocr=repl(ocr,"      fabricationDate: fabricationDate || '27/10/2026',", "      fabricationDate: fabricationDate || '',",'no fabricar fecha')
ocr=repl(ocr,"      fabricante: fabricante || 'GISER'", "      fabricante: fabricante || ''",'no fabricar fabricante')
put('js/ocr.js',ocr)

css=load('css/styles.css')
css=css.replace('--primary: #0284c7','--primary: #047857').replace('--primary-dark: #0369a1','--primary-dark: #064e3b').replace('--primary-light: #e0f2fe','--primary-light: #d1fae5')
css += '''\n/* GreenAir V2.1: accesibilidad y estados */
body { background: #f1f5f2; color: #25352e; }
.checkpoint-card { gap: 8px; }
.checkpoint-card:not(.checked) { border-color: #fca5a5; background: #fffafa; }
.qc-status { flex-shrink: 0; min-width: 76px; text-align: center; }
input:focus-visible, select:focus-visible, button:focus-visible { outline: 2px solid #e8821b; outline-offset: 2px; }
'''
put('css/styles.css',css)

manifest=load('android/app/src/main/AndroidManifest.xml')
manifest=re.sub(r'^\s*<uses-permission android:name="android.permission.(?:CAMERA|READ_EXTERNAL_STORAGE|WRITE_EXTERNAL_STORAGE|READ_MEDIA_IMAGES)"[^>]*/>','',manifest,flags=re.M)
manifest=repl(manifest,'android:icon="@android:drawable/sym_def_app_icon"','android:icon="@drawable/greenair_logo"','icono Android')
manifest=repl(manifest,'android:roundIcon="@android:drawable/sym_def_app_icon"','android:roundIcon="@drawable/greenair_logo"','icono redondo')
manifest=repl(manifest,'    </application>','''        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.files"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/file_paths" />
        </provider>
    </application>''','file provider manifest')
put('android/app/src/main/AndroidManifest.xml',manifest)
styles=load('android/app/src/main/res/values/styles.xml').replace('#0284c7','#047857').replace('#0f172a','#164e3a').replace('#10b981','#e8821b')
styles=repl(styles,'<item name="android:windowBackground">#164e3a</item>','<item name="android:windowBackground">@drawable/launch_background</item>','splash color')
put('android/app/src/main/res/values/styles.xml',styles)
put('android/app/src/main/res/drawable/launch_background.xml', '''<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@color/greenair_launch_bg" />
    <item><bitmap android:gravity="center" android:src="@drawable/greenair_logo" /></item>
</layer-list>
''')
put('android/app/src/main/res/values/greenair_colors.xml', '''<?xml version="1.0" encoding="utf-8"?>
<resources><color name="greenair_launch_bg">#164E3A</color></resources>
''')
put('android/app/src/main/res/values-v31/styles.xml','''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.GreenAirQC.NoActionBar" parent="Theme.GreenAirQC">
        <item name="windowActionBar">false</item>
        <item name="windowNoTitle">true</item>
        <item name="android:statusBarColor">#164e3a</item>
        <item name="android:windowSplashScreenBackground">#164e3a</item>
        <item name="android:windowSplashScreenAnimatedIcon">@drawable/greenair_logo</item>
    </style>
</resources>
''')
# Ensure Android app version number reflects replacement APK.
gradle=load('android/app/build.gradle')
gradle=repl(gradle,'versionCode 1','versionCode 3','versionCode 3')
gradle=repl(gradle,'versionName "1.0"','versionName "2.1"','versionName 2.1')
put('android/app/build.gradle',gradle)

readme=load('README.md')
put('README.md', '''# GreenAir QC V2.1 — Versión de correcciones (en validación)

Esta revisión agrega pedido en fichas, estado correcto/incorrecto, sonda CO₂ configurable,
cámara y galería separadas, limpieza segura y puente nativo para PDF/cámara.
No se ha probado aún en un teléfono real desde este entorno.
En Android se comparte el PDF como archivo y se incluye un texto con el resumen:
la aplicación receptora (WhatsApp/Gmail) puede ignorar ese texto según su versión.
La carga de Tailwind, jsPDF y Tesseract aún depende de CDN/internet.
La APK debe construirse desde Android/Gradle, nunca recompimiendo una APK existente.

---

''' + readme)

pkg=json.loads(load('package.json'))
pkg['version']='2.1.0'
pkg['scripts']['start']='node server.js'
put('package.json',json.dumps(pkg,ensure_ascii=False,indent=2)+'\n')
# Create updated SW cache identity without touching any entries.
sw=load('sw.js')
sw=re.sub(r"(const\s+CACHE_NAME\s*=\s*['\"])[^'\"]+",r'\1greenair-qc-v2-1',sw)
put('sw.js',sw)

# Files that can be safely replaced in whole.
for dest, content_base64 in EMBEDDED_OVERRIDES.items():
    modified[dest] = base64.b64decode(content_base64)

# Android icon is the original official asset, reused unchanged.
logo=root/'assets/greenair-logo.png'
if not logo.is_file() or logo.stat().st_size<100:
    raise RuntimeError('No está el logo oficial assets/greenair-logo.png; no sustituyo el icono por uno inventado.')
modified['android/app/src/main/res/drawable-nodpi/greenair_logo.png']=logo.read_bytes()

# All validations completed: now write files, with backups.
backup=root/'__backup_greenair_v2'
backup.mkdir(exist_ok=True)
for rel,content in modified.items():
    target=root/rel
    if target.exists():
        bak=backup/rel
        bak.parent.mkdir(parents=True,exist_ok=True)
        if not bak.exists(): shutil.copy2(target,bak)
    target.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(content,bytes): target.write_bytes(content)
    else: target.write_text(content,encoding='utf-8')
print('Corregidos', len(modified),'archivos en',root)
print('Respaldo en',backup)
print('Pendiente validar: compilación Android real, cámara física y envío WhatsApp. No borrar repositorio anterior.')
