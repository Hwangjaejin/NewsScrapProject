import requests # 크롤링 요청할 때 사용.(API 사용시 필요)
from bs4 import BeautifulSoup # 긁어 온 데이터를 잘 뽑아내기 위한 라이브러리

from pymongo import MongoClient
# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.newsdb
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


def insert_news():
    data = requests.get('https://news.naver.com/main/ranking/popularDay.naver?mid=etc&sid1=111',headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser') # soup : 해당페이지 html전체
    trs = soup.select('#wrap > div.rankingnews._popularWelBase._persist > div.rankingnews_box_wrap._popularRanking > div > div') # 웹에서 필요한 정보 우클릭 > 검사 > 해당영역 우클릭 > copy > copy selector

    for idx, tr in enumerate(trs, 1):
        base_url = 'https://news.naver.com'
        company_name = tr.select_one('a > strong').text
        company_logo = tr.select_one('a > span > img')['src']
        str = f'#wrap > div.rankingnews._popularWelBase._persist > div.rankingnews_box_wrap._popularRanking > div > div:nth-child({idx}) > ul > li'
        lis = soup.select(str)
        for li in lis:
            article_no = li.select_one('em').text
            article_title = li.select_one('div > a').text
            article_url = base_url + li.select_one('a')['href']
            if(li.select_one('a > img') is None):
                img_url = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUVFRgVFhIYGBgYGhoYHBwcGBodGR0aHxoaGRgaHBocIS4lHCErHxwYJjgmKzAxNTU1HCQ7QDs0Py40NTEBDAwMEA8QGhIRGDEdGCE0NDExNDE0MT80NDE0NDE0PzQ0NDQ/PzE0NDQ0NDExMT80MTExMTExMTExPzExMTExMf/AABEIAJ8BPgMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAAAQMEBQYCBwj/xAA6EAABAwIEAwYFAwMDBQEAAAABAAIRAyEEEjFBBVFhInGBkaGxBjJCwfAT0eEUUvFykrIHFTOCoiP/xAAYAQEBAQEBAAAAAAAAAAAAAAAAAQIDBP/EAB0RAQEBAQADAAMAAAAAAAAAAAABEQISITFBYXH/2gAMAwEAAhEDEQA/AOUIQuqBIlSIFQkQgVCQJUAhACteH8He+7rN5pbgqghaN/AaZs2tB66KDjOB1GAkDO3m37hTYKpCUhCoRCEQgEqRKgEIQgEBC5YC97WNElxhBNwGBfWflYO87AcytSW0sKzsiXEdp25PRO4ei3DUsg1iXHcnkFmONYslxJN7wOXX2/IWL1qyJLviN8zJ1jpc6df4Vi2szEsc2AHgGI/O5ef1sXBBJFvGPHcq9+HcbD23HcNeVzub+ihhqo2CRyTam8Tp5ajh1UNdIjlCVIgEhSohAiEqEZIhCEaCEqRBykXUJIRl0hKhGiIQhAIQhAkpUJUEvhlLO9rSrbjHERT7ABytEWVVwp5bVaRz05jdc8fJzkiDBP5f3Cz0Q2zifUkeEjyK0PD+LRBDsw0/gzv3rzutjCDYkX6/5V9wbEB4nNOxH1dZG/isq2WO4bTxDMzIa8eAPMRssjiaLmOLHiCFqMM7KMzXWOh6jQFccZw7K4APZfEsd9ik6z6ZrLIKYfULHZH68+cJupjmAarcsZxKRKgUMWX5mgQQAR17k7iC9rMxbbmCNOo74TyhlSWvCUlRKfD3PaX/AKhY6YA5wL/4TTGPL2Zj2DNwNCGzNus26KeUXxTKtTYePSd1ZfDOVjv1TfVjJ3PP3WexGYAtiSTqP7YtP5utBw2iXPa3ZsZeUwTPXX0WOutakxqc4c2Tf/F/Wyx3xJiGt3gamNT0H7ladgLOy4627p7X3K8y+J6zn1nH6STlG0C2izFRn4kPNm/t/JWn+HjpIJJNvuegCy2DozYbkT3brdcBwozNM+Hr6LUSnuOf+U9wVapXEKmao89YHgoy6xkkISohByQiEqEZIkSpECQiEqCjRChKhGSJAukiBVySgpUAhCVBzCUJUIEhKhEIHsK/K9p5EKV8QUpJI0N5HW91XhXNBorUontMt3j7rPUWMDiGGTefsm8FjP0nhxkDQxy3V7j8AZIiHazv+d6zPEqMHSDuI9Qubo9L4diCZl0ggQR8pkfkd6lOLxlyjOPUAmInz9FkPhCu4AMLjHywdiTYfcdR1W7wJgydJDT0iYPqfRBmuNcDqPOcG7XZx0AifPks47hz6cvezK02jUyRtfS+i9I4jigyA0A6j0geqzuJY6vIEiG5p62APiAVP4M7g6ZiNjBHjMeEtnzVg14DBmAjNGl9O1No536K6w2Eaxg7NyDaJaCQfITHmuTgC1oa9tiMp6E9mTbWfdMVB/SztdB+Q5nHYkS4yOuWFzh8EXNLg62YQI5mBfnaJ7lCwnETSP6BbnaKjpAF3NIETzkH3WnwrIFiIa4QALayB3RbxVFZg6GQvc4SPl0vEbjaSQrfAVGNgkQ3MMvKOYTbsO15dl7IcCTOttB0j7JurhC5jGB12xvadQfAR5hEaOo1riXa/wACFjOOfDwOeoTox3gA2bdS4+ikYLij4dfNL8szrAAge60NQtdTc2xkRG3KEHnXC8KGi+jdbXJ/tHMkrZYNmSk5/wBUGBsJUN3BHBwMy4axYX2b+/ep/FcM/wDRYxgPM+33SfUqgJQlNJzdQkXZkIQhGQkKVIgISQlQgRCVIjQSJUhRkJEqRAIQgIBKuSU2+rGyB0pM6r6mNA/bfwUR3EY0uE1cXT6gCUPWfq4oOtJBTdPFPBiZ81PIxpA4HdTOF4jJUEkQbGdFlGcRO+q7rcTsARfYhS2LjccWwIInLyIcL+KzLaTH12scJBOo57HumFrPhup/U4cB4cCNHG46XC4/7A4Euyh7gZ1Ikd/2K5tJOH4TTAs2DryIGwnp5JmriiCGg9ouNtJO48beKl4ivkZFwQPlOv8AIWf7dRxLQCHTLXag2+V3PTqix3QqOzOeZObsxqW6GY5yLq6fTcwQ1oJIm31A3cPW0pOHYJ/zOBL953FhHpqrrD4bMIktc3e0jlbRIlVNGoMxOoIImNpktI5iN0/xDBuqsJaSCd+83CluaHPyuAzAQbag2n85KYaWWkWkbR43QeXY/M+vTZ9TDkzRd0ECSB1B9F6HQ4c1jR2bs7U6ybGfQLzZ+JyYp9RwylxcGNA0IAAdHI2PmvU+BPzsaXEFxAB/2390Wq2vh2tidXQ6I56fdK/hZAJAyiLnfmfUqwxWGio13PUnYAQAFLe9rW5dY56k8/MojI4jghiJBM2mxjXwjmo7RUovFgWjUkgCfcrZDCNd2nXOsD+UxjsIwgy0ugTaPbmpYsqNgK7XS7s/mik1WNiY0ECdOpWdw1M0XBr5a0mQ2xd6aKyfic7bmGeU8pOkdFCqPirxm7MR3fnkqtwhaetSbctbtd0ekkQqPE023Mk9BEDpJC681ixDQgoW2QkKEFAIQhAISIQBSLpcoBIUqEAuSgyo1XERbQo0SvWjdQauKdsCUmIqB3NRKQOaRPrCzaSDtEp11ASMw13GniE7VeIDryNRHsucS9pbYiyx5NYV2Fy/My2xC4ewC4N5m64pcRIGRwkH88E3VDiJzeazauEfXbckC45780vChTLwHkRP1THoFW1Wdq9uo/ZXvw1w4PfM5u5pI8Z0V/CPQOG46gxoaw9waCfYSrejVcRmBHddUnDsO1tiBHQAR6T7K1c1oaQHkE/mqyKriTnPcDcEO2kzy8Vc4KmCMwie6TPWFX4Wg4kwGm/1e46+Su8KxwEE+w8uSsK6eyLxbuAHqZUHEcVY05s0WiRt/q7j0UX4nxv6dJ78wsD17t14hj+KV3vc/M4SbwYbOw74Vv6JHu/9UxzmEPBmDIcNQbju/ZXmJLXMcNbGb72XzRh+KVRDszgWnbz8V6H8L/E1R4LKj9i4HrG/PdS7Fk1xjqLLucIexzh0jZ/t5LUfBvFiRld9IzDnoAR3mJ8VheK4hpc75p29ST7eSm8JxuWSOz2Tby/YJb6axo/if47Yx4YxuYA3MxYLGY//AKiVi+WNAM733sI2Cp+KtL3hxNs19fOAoeJwlOkXsfmLw9pDmPYabqRAJg/MXSf3EqyazfT1j4M+KHYkZXnK4a2knr/gLbg2s6OsX8AvnXhfEHUxnpvcxwN4MDy329VtMD8eVIa17rCATAmE+GPQsewEaG15IBPuqtlcuMOmARFgJ9IUjAcYp12jK7W0HU6SdLKTVAn5b+vlspRExVRjW5nRI2n9jZZ/EYvOIAIjlp7keS0T+G55MuvrI26KvxPDvpIZlHeHeY+61zWaoZ6ohOYhmV0ekad/VcLqwRIV0UkIEQhCAQhCASJUhQIhCEEavWAHzQq52LzHL2Ty0lRMZUBP7rvDMb0nrdZ66akSn4b023R+o0CIgjkbeicZBHzdroQZ8CoTpzdrN5Fp8gudrchjEyTIJbfnI/hLRptsSTO/LvUz+kEHtDxTNUNHyjvtosqfdTY0TlLhpcKrxL3fSnazyBa562UEVidfzxVkTTD3ucdY9PNbP4Yw0MEOLi43dLhfk1oEnvlZ/hVL9R4a5rXf6psOruXeV6ZwPCspNgFpcLWaBbYCNB6laQ9hqLwYzQABa3j+SnquHc6e2ANLCPMqY3CNdclwP5oE5U/Ta29T88FBAa5lNtwB1H3ssxxj4u/ScQxxB6QWkbSl+J+N02NLQ5wOxER5TbvXm2Jql7i4k37gpirXivGH4h0vqEjlt5Kkdinte0hsZHB7RAc2QQbgiDpoVw825R+dyco1AfoB71qehKLmvY5xZ23PL3GwbB+lrAIFyT5BXfBOH1Hw5gsB+BROC4B+JeKbRDRcxYf55L2TgPA2UGQ0d9umvss9Xfiz086xnCi58EGRBP310uCp3C+AkOAJ7Pt0Wk48+nSeCSGkzy/NVT1/iOiwH/8ARszt5rjnTflBxX4GLhNI63v3T+d6xPGOBvoOAq0yLCCNDPVe3fDvE6eJph7CDsRyPIp3jfBaeIpuY5okiAYuO5duZZGL0+c3MiQ0QEmfkPFaP4n4BXwz8hpyxxIZHaLusC8qspcHxD9KThbeG++iom/D3HjQfcSLA3PovSeGccp1R80HkQfuYXlj+DtZH6lemD/ax4e4d8QB5q64JjKFMgCXRbM4z/8AMAD1RHq1CsHj6Y5Ae91HxrCQYZmAHQeUXUHhmPa8ANE7WFvtHkrV1JhGYlwPQx7pErHYikGuuHTy28zdMOceQb+eZV9xWi1/ymXcxpHifULPPaQbz4rpzWKWy5KEhK0hVyVAxvFmMOX5ncgob+KgPDv1AWn6Ivpv4rN6kWRdylVNgOLZn5HNgm45+PJXIVl0sIkXRSKoRIUqEGaw+GAbLgL81Ka7LZrw09N0OYx3ykt/OiQ4Ldz+42IXC11MgmdjPRWNMMcLvdNhBccvmijTY27nB28kLjE1WRmY0A6WlKQ6+mxvJp6GR4bquxRBJyXPeV0yq83kADaNu5NYmoDvJ6AqKr303meyuAyPmFu9SXukXOvKfuohqQbbLURpPh/hzXdu7GjUmDI6Bt16Fw0siGvcT1mY6N2Xm3BKDXQ57yN82eT3NZB8yvR+G1mhgDQ8DrAcepkfYBLUWFela0fcrE/EeMewH7uB8gLrUY/EiIDpJ2zCf+QWI47QYZzPa3mM9OfHthS1ZGKxmMdUJzuI5SokW+byEhWlTh9Kb4ljR3A/8XlcNo4YWNd7/wDRTj/mtFVhJ1AhPYetcZm+UA/srNjMMNKNUjm+sxg8ms+6vOBcMZUe0inRABBPaqud5vcA7wCg23/T/hGSiKhYAXibgZiNrgn85LaPrNYxzjADQSe4KLh3DK0AxAtsofFXOex7CPma5sjaREq4zryP4p+If6qpnnKzRjZvl5nqfuq+nhKMAuqSCCbcxBi6pMbhYe5ryWuaYI6jomXVosDYKqu+HcYOHqt/QqOY6RMHXv5jove+BcV/qMPTqxBe24HMEh3qF864BuZ2VjJe+32le6fDcUaDKTSHZGgE7E6mPFQq24rhjUY5oflJtIJBHiNF5Lxr4be0mXseRs6uW6/6yvWTiWgQT978l538aY6oHlgktAkhj4dFr5SHNI6x5KUjFO4ZVJgUSejXsf5ZZTTsBVYQXUKjO9rvfKpIfSfqASdnNIP++mSP/gJ5mEI7bKjmdzs7f97NPEBGmj+F+JNZGckeJJ8lsX8XYRAdM8wY8iFh8FVrFsF5fzIh48zMeKvcFUAHaYy/OzvCFlLDnFKmYZg0eoPTSZCqxULtVKx7qbgf/IL/AEw4d+U5Y8CmsNhwRP6jYOmYFpPgV15rPUNPeGgkmANSslxXjD6kimSGNnTV38Kd8S4gnsB8N+ohjzPQHLEeKomZD2A+5tOUj9066/EOYjtxIF7ydB7J5jgBOpPmSgcLAtmvs6QfJRqFNzX5R2nXvOl/RYaaDgLSKgJ+qZ8p+0LUyqH4fomSXQTA8FfLpz8Y6+kKRKUi0yEIQgoywN0mOV/bZc5Q60weoXb8O7NLB4n73UnI4/OY6ER/lcXVHe8tENa4kaGxamWYh7ndoCTvEeFk+6m6bPDgNsrojwSF7gbkNGmn8Ss6qU+s4NGgta37aqrribl1+unpdTHVGkfUegkCPEeyg1Qf7fKPWEgi1GjQEkhMOad7Lus487JlsTcT+eq0i++H3w4OLy0DUm3rsF6JhatPIId43knWb9/+F57wlwkONMOjQbDv29FqsJiA8w8t/wBMkzvENENHes2iTinMPyie4yTzJIM+yyPGaToPYidLEe5Mrb1MSNOyABeCOVhAVLintJPaN7CBM+izqx5tiaBBv7rktyj5jPt3LX4nhDC753Fx79eUNXLOCU2GJD6huASC0HumHeNu9blMZzB4OS19R2VjjaxL39GNF3cp06r0b4cxdJgyMptaCYu4l0jUamTOzRbdUY4VmMgkvdZzhZztsjCbtbsXeASvwzqREhskZZHytb/YzpzO8HrLUelMrNLQc090a96r+JV7ENqX2kSPRZP/ALuX5GAFoMRqOybMv3X/APZBxDnyf1DB0g2jb0WtZxR/FNJr3FxptLh9TMwMbSswOHxciO9bHE8ILh/5HAEm0nkN/BRmcDaDJ7U63PO3uprSu4UxjHSDto0TOhFyt7wjiVV1gw5Rz9o2VTw/hbGatsrapxNlNpAF27c+nRTTE3E4lzTL7g2M6DkVnMezO/tAw07atOhLTPpoe+6hYzjzajiyeomQfz7SuKHHmQ2RGYZSTe7ba7H5fNQieeAMe3O0gu5gCDzBAIIcusDwxrTmdIPMFw99fNVlPirmPc+mQ9p1afm7pEF0dbj1UpnE6j+02HN3BADh0dFiOseSVYuTTps7UkH+4R6tBg+ACZd2rgZm65gQD4iLfl1HwjM7pNumQH/jKt/6ZrQHD0lpUhaqahkgkSO+/iNPLkovE8RlpvfvGUTqrl7KDruIE8p16gWWZ+IS0N0JbfLJMR4arcuIz2CMAnMQRyJE/uuv1w4nsNJ5gZTqNxZR8mbQnrCnUGtEDpEHdFd4RrBMyOUn7pnC4R1SqWsbF5LtoTjO04NymdAFqcBhAxgG5uT1V5m1m0uCwoptyi/M8ypCEq6sUhCSF0hEcoSwiEEHD1GgmG//AEde5du7QtJdveSlaGk3LgO6w9UVWuBll+sCY71xdTYqllgbmBEGfOIC5dWaBGjjsJc7xJUgVzEGR0I8zKYfUY2wBk6kwT6LNVXYsvPzOgbD2tsoj8wEzblzKscWGNuTLjtp3KrrVXExCCPVfOplJhqZLhbfeyeYwC7j5fup1PDgAOEye+yuph8NcBlDgD77baK74VRIETaLw0a/kKFhcOyAHZi47Akk+X7rQU6DGNhzhp8jZt0IGg5zKytOUmsa0yQQLne/XmVX1Je7sTJ8LfYd6sGAEBthNw0CIG5M6C8yeaj1KpLslOzZuZOY/wCfupmmqXGS0ljCS82Lp8wJ0HM+fJVeIeGAkzk+t8S551/TYDaO/vOwWgGRkszZ3H53TI6N1vcG25uomIpNfLnMhjOep0OVoG5sOQHcrPSqpnHSwCo8ZWR2GNscuw0+Z1zyDb/UFDd8RvxLzmYGMAMxqGRLr/6A4DwTXGqD6jy9wAmzWt+VrRo1oVayiWU3mCMxaweYc70aB/7LWs4dwfEc9dri2CXzzgC8dAAIjorHBcXgNgOMXjTxP7LPYcODi4WysefHI4D1ITLHOEfhn83VVu3cUAAJMAtBHn7p2nj5bm0Gw3vYfbzWQfiQ5rQSRFxAsbkc+gKHYh5DQJGXS82vrO9yspjTN43AMkb2Mdd/Aqjx/GX1OTY3m5Hgo/bIDYB1m3P3URmEefpnwV0w6ajiQ7Rw/LKWcNnBiRMVAOujx538FxhsFcAj3VxhqYaQI06c7FNXDOAwuWDJB9/3Wm4dkN/lfz2dzBB9fuqRgZmywRyhWGFc1pG/MHy1UK0dBjYuBlPITB7/AMKdqMyCWPkcnGCO4woGGqZO02nryJv3gKwpvBs5p7W2sRzPJEqrxbgTlyiTrH8LOcbY5ulgdQdJ7lqXsAd2WgDU8z5aKFxfBB7Ta2mmnJaGSyNy9kdSD9iNQuWwLlR6j30zlLSYNirvgfDHVTne2Gi4HM7FBK4Lgi0Z3jtHToFbFOOZC4K6yZHOkQhCqBCEIFQkQg4dg7bz3/uoFR5Y4huvTT+VJxWTRzng8gbQowIjtP10GU+4K4urim97rOvPIAeqe/TA01H5rFkEMaLOcO7uklQ6sEECeeqyGsY6+wI3F/L91XOi9p6lSMSQ0ZQL7n0TLm2N94WlOYFmY3BPIR6K9o4RzoBt4aKDwkNF3TET+QtJgsI94DoABMNE+sc+9YobpAM0gnSdgPv3IrMcRlBcJ1IEQN3HlsBvfdWtTDmzRDRF4F9JJnnCrOO4sUmZWnKegk3MC51Ot+qkDD6hz/psYDIi/aeYuSSdgbRe5UhmHIaSXQLlziOkwPy3il4ThnUmy4y6BJJLjJJPcd+miTE4qZJBDZDRBGYmJPRogegWtELFuDGdmGtFwPqcep27+qrsbXeQxryGgjM6BYNAs1o21P8AvUvFcRz5iAR+mJN7STAPNxF+QVXXoF1S+ZxPaMu+mSQB5eyIYr4qnpJ0A3J21ATPEabYYwSbF2l+0Y9mjzUl/CCKZq75nCLa5oB8/ZdY7Bw4scfpaDHNsNPTUFXDVP8AoN7XaElv3aov9GNRfqpuIptAdF+XTtCR6JqlVuHRaSI6x/hRXLMM2B0n9/3UltJt0jG3nkCSOnROtMmN/DuUU3RYZsbeX8KypMbG08tfI8lDLNi688pTrKBsfCUHbXskjpr7pKBIMSHDYzB10P5ZOswZcCYgi+102OwBI+bSYO11USWUw4gAF0bCZHlqrXDYN2uQHlYyB1zaeCrKWJe4dl0DTceysaIAIzEGeQM+coLCk/KfqtycSO7LpKkOx4YCCNdf5IUc03HtNZ3dod267GGeIbUgl3yjWCLAzK0h3DY1pdLBmB11I0vCdxNeB22jKba36W5LmngmtM5iS43J2OkBTf0CBLspHcVPgzj8Iyq+7b6CxvylaTD4RrWRp4WRhWf202t5J/EvIGkqSbS30p8ZqoSk4l5Jv9lGXonxyCEJECoSIQKlSIQf/9k="
            else:
                img_url = li.select_one('a > img')['src']
            time_ago = li.select_one('div > span').text

            doc = {
                'company_logo':company_logo,
                'company_name':company_name,
                'article_no':article_no,
                'article_title':article_title,
                'article_url':article_url,
                'img_url':img_url,
                'time_ago':time_ago,
                'view': 0
            }
            db.news.insert_one(doc)
            db.allnews.insert_one(doc)

def insert_headline():
    data = requests.get('https://edition.cnn.com/',headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    trs = soup.select('#intl_homepage1-zone-1 > div.l-container > div')
    print(trs)
    for tr in trs:
        # img_url = tr.select_one('article > div > div.media > a')['href']
        # img_text = tr.select_one('div > p').text
        print(tr)

# 기존 newsdb 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    # db.news.drop()  # mystar 콜렉션을 모두 지워줍니다.
    # insert_news()
    insert_headline()


### 실행하기
insert_all()