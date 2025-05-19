import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from redis.asyncio import Redis
import string
from datetime import timedelta
import ssl
import time

from config.env import EmailConfig


class EmailService:
    """
    邮件服务类
    """
    
    @staticmethod
    async def send_refund_notification_email(email: str, user_info: dict, order_info: dict, refund_info: dict):
        """
        发送退款通知邮件
        
        :param email: 接收邮箱
        :param user_info: 用户信息
        :param order_info: 订单信息
        :param refund_info: 退款信息
        :return: (发送结果, 错误信息)
        """
        last_exception = None
        MAX_RETRIES = 3  # 最大重试次数
        RETRY_DELAY = 2  # 重试延迟（秒）
        
        # 构建状态文本
        status_text = "已通过" if refund_info.get("approved") else "已拒绝"
        status_color = "#009933" if refund_info.get("approved") else "#ff0000"
        
        # 构建邮件内容
        subject = f"【HK Tax AI Chat】退款申请{status_text}"
        message = f"""
        <div style="background-color:#f8f8f8;padding:20px;">
            <div style="max-width:600px;margin:0 auto;background-color:#fff;padding:30px;border-radius:6px;box-shadow:0 2px 10px rgba(0,0,0,0.1);">
                <h2 style="color:#333;font-size:20px;margin-bottom:20px;">退款申请{status_text}</h2>
                
                <div style="margin-bottom:20px;border-bottom:1px solid #eee;padding-bottom:15px;">
                    <h3 style="font-size:16px;color:#555;">用户信息</h3>
                    <p style="margin:5px 0;color:#666;">用户ID: {user_info.get('user_id', '')}</p>
                    <p style="margin:5px 0;color:#666;">用户名: {user_info.get('user_name', '')}</p>
                </div>
                
                <div style="margin-bottom:20px;border-bottom:1px solid #eee;padding-bottom:15px;">
                    <h3 style="font-size:16px;color:#555;">订单信息</h3>
                    <p style="margin:5px 0;color:#666;">订单ID: {order_info.get('payment_id', '')}</p>
                    <p style="margin:5px 0;color:#666;">产品名称: {order_info.get('product_name', '')}</p>
                    <p style="margin:5px 0;color:#666;">原订单金额: {order_info.get('original_amount', '')} {order_info.get('currency', '')}</p>
                </div>
                
                <div style="margin-bottom:20px;border-bottom:1px solid #eee;padding-bottom:15px;">
                    <h3 style="font-size:16px;color:#555;">退款信息</h3>
                    <p style="margin:5px 0;color:#666;">退款金额: {refund_info.get('refund_amount', '')} {refund_info.get('refund_currency', '')}</p>
                    <p style="margin:5px 0;color:#666;">退款状态: <span style="color:{status_color};font-weight:bold;">{status_text}</span></p>
                    <p style="margin:5px 0;color:#666;">原因: {refund_info.get('confirm_reason', '')}</p>
                </div>
                
                <div style="margin-top:30px;padding:15px;background-color:#f9f9f9;border-radius:4px;">
                    <p style="margin:0;color:#666;font-size:14px;">
                        {
                            "如您的退款申请已通过，款项将在3-5个工作日内退回您的支付账户。" 
                            if refund_info.get("approved") else 
                            "如有疑问，请联系客服。"
                        }
                    </p>
                </div>
                
                <p style="margin-top:30px;color:#999;font-size:12px;">此邮件由系统自动发出，请勿回复。</p>
            </div>
        </div>
        """
        
        # 发送邮件
        msg = MIMEText(message, 'html', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = EmailConfig.email_from
        msg['To'] = email
        
        # 尝试发送邮件，最多重试MAX_RETRIES次
        for attempt in range(MAX_RETRIES):
            try:
                if EmailConfig.email_use_ssl:
                    context = ssl.create_default_context()
                    # 禁用SSL证书验证
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    
                    with smtplib.SMTP_SSL(
                        EmailConfig.email_host, 
                        EmailConfig.email_port, 
                        context=context,
                        timeout=30  # 设置超时时间为30秒
                    ) as smtp:
                        smtp.login(EmailConfig.email_username, EmailConfig.email_password)
                        smtp.sendmail(EmailConfig.email_username, email, msg.as_string())
                else:
                    with smtplib.SMTP(
                        EmailConfig.email_host, 
                        EmailConfig.email_port,
                        timeout=30  # 设置超时时间为30秒
                    ) as smtp:
                        # 尝试使用STARTTLS进行安全连接
                        try:
                            smtp.starttls()
                        except:
                            pass  # 如果服务器不支持STARTTLS，则继续使用非加密连接
                        smtp.login(EmailConfig.email_username, EmailConfig.email_password)
                        smtp.sendmail(EmailConfig.email_username, email, msg.as_string())
                
                print(f"退款通知邮件已发送到邮箱 {email}")
                return True, ""
                
            except Exception as e:
                last_exception = e
                error_message = str(e)
                print(f"发送退款通知邮件尝试 {attempt+1}/{MAX_RETRIES} 失败: {error_message}")
                
                # 如果不是最后一次尝试，则等待后重试
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
        
        # 所有尝试都失败后，返回错误信息
        error_type = str(last_exception)
        print(f"发送退款通知邮件最终失败: {last_exception}")
        
        # 根据错误类型返回用户友好的错误信息
        if "authentication" in error_type.lower() or "auth" in error_type.lower():
            return False, "邮件服务器认证失败，请联系管理员"
        elif "timeout" in error_type.lower():
            return False, "邮件服务器连接超时，请稍后再试"
        elif "recipient" in error_type.lower() or "mailbox" in error_type.lower():
            return False, "收件邮箱地址有误，请检查后重试"
        elif "connect" in error_type.lower() or "network" in error_type.lower() or "closed" in error_type.lower():
            return False, "网络连接异常，请检查网络后重试"
        else:
            # 默认错误消息
            return False, "邮件发送失败，请稍后重试" 