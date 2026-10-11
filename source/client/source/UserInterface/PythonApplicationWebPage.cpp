#include "StdAfx.h"
#include "PythonApplication.h"
#ifdef ENABLE_CEF_BROWSER
#include "CefWebBrowser.h"
#endif

bool CPythonApplication::IsWebPageMode()
{
#ifdef ENABLE_CEF_BROWSER
	return CefWebBrowser_IsVisible() ? true : false;
#endif
}

void CPythonApplication::ShowWebPage(const char* c_szURL, const RECT& c_rcWebPage)
{
#ifdef ENABLE_CEF_BROWSER
	if (CefWebBrowser_IsVisible())
		return;
#endif

	m_grpDevice.EnableWebBrowserMode(c_rcWebPage);

#ifdef ENABLE_CEF_BROWSER
	if (!CefWebBrowser_Show(GetWindowHandle(), c_szURL, &c_rcWebPage))
#endif
	{
		TraceError("CREATE_WEBBROWSER_ERROR:%d", GetLastError());
	}

	SetCursorMode(CURSOR_MODE_HARDWARE);
}

void CPythonApplication::MoveWebPage(const RECT& c_rcWebPage)
{
#ifdef ENABLE_CEF_BROWSER
	if (CefWebBrowser_IsVisible())
#endif
	{
		m_grpDevice.MoveWebBrowserRect(c_rcWebPage);
#ifdef ENABLE_CEF_BROWSER
		CefWebBrowser_Move(&c_rcWebPage);
#endif
	}
}

void CPythonApplication::HideWebPage()
{
#ifdef ENABLE_CEF_BROWSER
	if (CefWebBrowser_IsVisible())
	{
		CefWebBrowser_Hide();
#endif

		m_grpDevice.DisableWebBrowserMode();

		if (m_pySystem.IsSoftwareCursor())
			SetCursorMode(CURSOR_MODE_SOFTWARE);
		else
			SetCursorMode(CURSOR_MODE_HARDWARE);
	}
}